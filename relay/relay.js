// sc3 relay — tiny room-scoped WebSocket fan-out for the Session Companion.
// Zero dependencies: plain Node (v16+), no npm install needed.
// Every message is forwarded to the other sockets in the same room; nothing is
// stored or logged. Run:  node relay.js   (listens on 127.0.0.1:8787; Caddy adds TLS)
"use strict";
const http = require("http");
const crypto = require("crypto");

const PORT = 8787, HOST = "127.0.0.1", MAX_PAYLOAD = 256 * 1024;
const GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11";
const rooms = new Map(); // room -> Set<client>

const srv = http.createServer((req, res) => { res.writeHead(200, {"content-type":"text/plain"}); res.end("sc3 relay up\n"); });

srv.on("upgrade", (req, sock) => {
  const key = req.headers["sec-websocket-key"];
  const room = (new URL(req.url, "http://x").searchParams.get("room") || "");
  if (!key || (req.headers.upgrade || "").toLowerCase() !== "websocket" || !/^[\w-]{4,64}$/.test(room)) {
    sock.write("HTTP/1.1 400 Bad Request\r\n\r\n"); sock.destroy(); return;
  }
  const accept = crypto.createHash("sha1").update(key + GUID).digest("base64");
  sock.write("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: " + accept + "\r\n\r\n");
  sock.setNoDelay(true);

  let set = rooms.get(room);
  if (!set) { set = new Set(); rooms.set(room, set); }
  const c = { sock, alive: true, buf: Buffer.alloc(0), frag: null };
  set.add(c);

  const bye = () => { set.delete(c); if (!set.size) rooms.delete(room); try { sock.destroy(); } catch (_) {} };

  sock.on("data", (chunk) => {
    c.buf = Buffer.concat([c.buf, chunk]);
    if (c.buf.length > MAX_PAYLOAD * 2) return bye();
    for (;;) {
      const f = readFrame(c.buf);
      if (!f) break;
      c.buf = c.buf.slice(f.size);
      if (f.payload.length > MAX_PAYLOAD) return bye();
      switch (f.op) {
        case 1: case 2: // text/binary (possibly fragmented)
          if (!f.fin) { c.frag = f.payload; break; }
          relay(set, c, f.payload); break;
        case 0: // continuation
          if (c.frag == null) return bye();
          c.frag = Buffer.concat([c.frag, f.payload]);
          if (c.frag.length > MAX_PAYLOAD) return bye();
          if (f.fin) { relay(set, c, c.frag); c.frag = null; }
          break;
        case 8: try { sock.write(frame(8, f.payload.slice(0, 2))); } catch (_) {} return bye();
        case 9: try { sock.write(frame(10, f.payload)); } catch (_) {} break; // ping -> pong
        case 10: c.alive = true; break; // pong
        default: return bye();
      }
    }
  });
  sock.on("error", bye);
  sock.on("close", bye);
});

function relay(set, from, payload) {
  const out = frame(1, payload);
  for (const peer of set) if (peer !== from) { try { peer.sock.write(out); } catch (_) {} }
}

// parse one client->server frame (client frames are masked per RFC 6455)
function readFrame(buf) {
  if (buf.length < 2) return null;
  const fin = !!(buf[0] & 0x80), op = buf[0] & 0x0f, masked = !!(buf[1] & 0x80);
  let len = buf[1] & 0x7f, off = 2;
  if (len === 126) { if (buf.length < 4) return null; len = buf.readUInt16BE(2); off = 4; }
  else if (len === 127) { if (buf.length < 10) return null; const big = buf.readBigUInt64BE(2); if (big > BigInt(MAX_PAYLOAD)) return { fin, op: 8, payload: Buffer.alloc(0), size: buf.length }; len = Number(big); off = 10; }
  const maskLen = masked ? 4 : 0;
  if (buf.length < off + maskLen + len) return null;
  let payload = buf.slice(off + maskLen, off + maskLen + len);
  if (masked) { const m = buf.slice(off, off + 4); const p = Buffer.from(payload); for (let i = 0; i < p.length; i++) p[i] ^= m[i & 3]; payload = p; }
  return { fin, op, payload, size: off + maskLen + len };
}

// build a server->client frame (unmasked)
function frame(op, payload) {
  const len = payload.length;
  let head;
  if (len < 126) { head = Buffer.from([0x80 | op, len]); }
  else if (len < 65536) { head = Buffer.alloc(4); head[0] = 0x80 | op; head[1] = 126; head.writeUInt16BE(len, 2); }
  else { head = Buffer.alloc(10); head[0] = 0x80 | op; head[1] = 127; head.writeBigUInt64BE(BigInt(len), 2); }
  return Buffer.concat([head, payload]);
}

// heartbeat: ping every 30 s, drop sockets that never pong back
setInterval(() => {
  for (const set of rooms.values()) for (const c of set) {
    if (!c.alive) { try { c.sock.destroy(); } catch (_) {} continue; }
    c.alive = false; try { c.sock.write(frame(9, Buffer.alloc(0))); } catch (_) {}
  }
}, 30000);

srv.listen(PORT, HOST, () => console.log("sc3 relay on " + HOST + ":" + PORT));
