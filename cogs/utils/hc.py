from discord import http
from discord.http import Route


def send_message(
    self,
    channel_id,
    content,
    *,
    tts=False,
    embed=None,
    embeds=None,
    nonce=None,
    allowed_mentions=None,
    message_reference=None,
    components=None,
):
	r = Route('POST', '/channels/{channel_id}/messages', channel_id=channel_id)
	payload = {}

	if content:
		payload['content'] = content

	if tts:
		payload['tts'] = True

	if embed:
		payload['embeds'] = [embed]

	if embeds:
		payload['embeds'] = embeds

	if nonce:
		payload['nonce'] = nonce

	if allowed_mentions:
		payload['allowed_mentions'] = allowed_mentions

	if message_reference:
		payload['message_reference'] = message_reference

	if components:
		payload['components'] = components

	return self.request(r, json=payload)


def send_files(
    self,
    channel_id,
    *,
    files,
    content=None,
    tts=False,
    embed=None,
    embeds=None,
    nonce=None,
    allowed_mentions=None,
    message_reference=None,
    components=None,
):
	r = Route('POST', '/channels/{channel_id}/messages', channel_id=channel_id)
	return self.send_multipart_helper(
	    r,
	    files=files,
	    content=content,
	    tts=tts,
	    embed=embed,
	    embeds=embeds,
	    nonce=nonce,
	    allowed_mentions=allowed_mentions,
	    message_reference=message_reference,
	    components=components,
	)


def do():
	http.HTTPClient.send_message = send_message
	http.HTTPClient.send_files = send_files
