{% from 'picture.j2' import picture_light_dark %}
{% from 'note.j2' import note %}
Title: Sending a webhook from Synology DSM to Discord
Date: 2022-01-17
Category: Programming
Description: Rapid walkthrough of how to send push notifications from your Synology NAS to Discord via webhooks.
Tags: synology, self-hosting
Keywords: synology, discord, webhook, dsm

Sending webhooks notifications from a Synology NAS to Discord is technically possible, but the DSM UI somehow seems to prevent us from doing so, as documented in this [forum thread](https://www.synoforum.com/threads/webhooks-to-post-alerts-messages-on-to-discord.6725/#post-32618). Somehow, we _have_ to include a `hello world` message in the notification, as part of the message content, without which, the UI won't allow us to save the webhook configuration.

You can however circumvent the issue by `ssh`-ing into the NAS and edit the `/usr/syno/etc/synowebhook.conf` into this:

```json
{
    "Discord": {
        "needssl": false,
        "port": 8090,
        "prefix": "A new system event occurred on your %HOSTNAME%",
        "req_header": "",
        "req_method": "post",
        "req_param": "{\"username\":\"Synology\", \"avatar_url\": \"https://play-lh.googleusercontent.com/HjbYWbXJ-6e6Cia-mBbHDSdontW1yE6MHMaXqlHW80CQegDOEPQ1HGACxvEpnqCUHgo\", \"embeds\": [{\"description\": \"@@TEXT@@\", \"title\": \"@@PREFIX@@\"}]}",
        "sepchar": " ",
        "template": "$webhook_url",
        "type": "custom",
        "url": "$webhook_url"
    }
}
```
{{ note("<b>Note</b>: replace `$webhook_url` by your Discord webhook URL.") }}

When this is done, you should see a `Discord` webhook in your Webhook Push Services, and you should now be able to send a test message to Discord!

{{ picture_light_dark("syno-discord/light/discord-notif.webp") }}
