# Hosting the Session Companion

The companion is a plain static folder — any static web host serves it unchanged
(index.html fetches everything by relative path). Three things to know first:

1. **The two windows must still run on ONE computer.** The participant display and
   the ?host console sync through the browser itself (BroadcastChannel), which only
   works between windows of the same browser on the same machine. Hosting changes
   where the files come from, not this. Remote participants see the participant
   window via Teams/Zoom screen-share, exactly as before.
2. **The bundle contains researcher material.** bundle/pool_manifest.json holds the
   keys and evidence lines, and ?host is just a URL parameter — anyone who has the
   site URL can see both. On a public host, treat the URL as confidential, or put
   the site behind a password (options B/C below do this properly).
3. **Use ONE address forever.** Saved sessions (crash-resume) live in the browser,
   keyed by the site's address — https://vis.example.com and the same site at
   another address keep separate saves. Pick the final URL before the first real
   session. (Old localhost test saves will not follow you; that's fine.)

## Option A — GitHub Pages (free, no auth)
You already run omgitsamir.github.io, so this is the lowest-friction route.
    cd companion/
    git init && git add -A && git commit -m "session companion"
    # create a PRIVATE repo named e.g. session-companion, then:
    git remote add origin git@github.com:omgitsamir/session-companion.git
    git push -u origin main
    # GitHub → repo → Settings → Pages → Deploy from branch → main / root
Site: https://omgitsamir.github.io/session-companion/
Caveats: the PAGE is public even when the repo is private (private Pages needs
Enterprise); there is no password. index.html now carries a noindex meta tag, so
search engines won't list it — but anyone with the URL sees everything, keys
included. Fine if you keep the URL to yourself; not fine if you'll share it.

## Option B — your VPS with a password (recommended)
Full control, real auth, ten minutes with Caddy (auto-HTTPS):
    rsync -av companion/ user@your-vps:/srv/companion/
    # on the VPS:  caddy hash-password   (enter a password, copy the hash)
    # /etc/caddy/Caddyfile:
    companion.yourdomain.com {
        root * /srv/companion
        file_server
        basic_auth {
            amir <paste-hash-here>
        }
    }
    sudo systemctl reload caddy
One password gates the whole site (keys, console, everything). nginx equivalent:
`auth_basic` + htpasswd. Updating = re-run the rsync.

## Option C — Cloudflare Pages + Access (free, real auth, no server)
    https://pages.cloudflare.com → create project → direct upload → drag the
    companion folder in. Site: https://<name>.pages.dev
Then Zero Trust → Access → add an application for that hostname with a policy
allowing only your email (one-time PIN login). Free for up to 50 users. Gives you
GitHub-Pages convenience with a genuine login in front of it.

## Option D — Netlify Drop (fastest throwaway)
    https://app.netlify.com/drop → drag the folder → instant URL.
Good for showing Mai a one-off preview; password protection is a paid feature, so
don't leave study material parked there.

## After deploying, verify once in the hosted copy
Open the hosted URL: welcome shows → ?host: start a test session → an interactive
chart loads (S2) → Inspect the data opens → export downloads. Delete the test
save (DevTools → Local Storage) before the first real participant.
