# Remote two-computer sessions (room mode)

Room mode lets the participant open the companion on **their own computer** while your
`?host` console drives their screen — and their clicks (intake answers, data/code opens,
ratings) flow back to you. State travels through a tiny relay on your VPS over TLS;
the relay forwards messages within a room and stores nothing.

Without a `room` in the URL, nothing changes: same-machine sessions keep using the
browser's own sync exactly as before.

## 1 · One-time VPS setup (~5 min)

The relay has **no dependencies** — it only needs Node itself, no npm.

```bash
# from your Mac, inside the companion/ folder:
ssh ubuntu@135.125.204.206 'sudo apt install -y nodejs && sudo mkdir -p /srv/sc3-relay && sudo chown ubuntu: /srv/sc3-relay'
scp relay/relay.js relay/sc3-relay.service ubuntu@135.125.204.206:/srv/sc3-relay/

# then on the VPS:
sudo cp /srv/sc3-relay/sc3-relay.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now sc3-relay
systemctl status sc3-relay          # active (running)
curl http://127.0.0.1:8787/        # "sc3 relay up"
```

## 2 · Caddy: expose the relay at /sync (same hostname, no basic-auth on it)

Replace your site block in `/etc/caddy/Caddyfile` with:

```
YOUR-HOSTNAME {
    @sync path /sync
    handle @sync {
        reverse_proxy 127.0.0.1:8787
    }
    handle {
        root * /srv/companion
        file_server
        basic_auth {
            amir YOUR-EXISTING-HASH
        }
    }
}
```

Then `sudo systemctl reload caddy`. Check: `curl https://YOUR-HOSTNAME/sync` → "sc3 relay up".
(The /sync path skips the password on purpose — browsers can't answer a basic-auth
prompt for WebSockets. Rooms are unguessable random codes, the relay only forwards
within a room, and it never serves the study files.)

## 3 · Point the app at the relay

In `index.html`, set one line in CONFIG:

```
 sync_server: "wss://YOUR-HOSTNAME/sync",
```

Redeploy wherever the app lives (GitHub Pages: commit + push; VPS copy: rsync).
The GitHub Pages copy and the VPS copy can both use the same relay.

## 4 · Running a remote session

1. Open your console as usual (`…/index.html?host`). The setup screen now has a
   **Remote session** card → **Create room**. The page reloads with a room code and
   shows the **participant link**.
2. Send the participant link (it carries the room code, no `host`) to the participant;
   they open it on their machine. A status pill bottom-right shows
   "participant · room … · connected" on their side and the same on yours.
3. Run the session exactly as normal. Their intake answers mirror into your console,
   your stage changes repaint their screen, and their data/code/zoom clicks are logged.
4. Resume works: reopen the SAME console URL (keep the room code in it) and click
   Resume — the participant rejoins with their same link.

Caveats: the room code is the only key to the live session, so share the link only
with the participant. Export still happens on YOUR machine (the console holds the
session). If the pill goes red mid-session it reconnects by itself within ~2 s.
