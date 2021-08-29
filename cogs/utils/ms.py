from __future__ import annotations

import copy
import asyncio
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    TYPE_CHECKING,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
    runtime_checkable,
)

from discord.iterators import HistoryIterator
from discord.context_managers import Typing
from discord.enums import ChannelType
from discord.errors import InvalidArgument, ClientException
from discord.mentions import AllowedMentions
from discord.permissions import PermissionOverwrite, Permissions
from discord.role import Role
from discord.invite import Invite
from discord.file import File
from discord.voice_client import VoiceClient, VoiceProtocol
from discord import utils

T = TypeVar('T', bound=VoiceProtocol)

if TYPE_CHECKING:
	from datetime import datetime

	from discord.user import ClientUser
	from discord.asset import Asset
	from discord.state import ConnectionState
	from discord.guild import Guild
	from discord.member import Member
	from discord.channel import CategoryChannel
	from discord.embeds import Embed
	from discord.message import Message, MessageReference, PartialMessage
	from discord.channel import TextChannel, DMChannel, GroupChannel
	from discord.threads import Thread
	from discord.enums import InviteTarget
	from discord.ui.view import View
	from discord.types.channel import (
	    PermissionOverwrite as PermissionOverwritePayload,
	    GuildChannel as GuildChannelPayload,
	    OverwriteType,
	)

	PartialMessageableChannel = Union[TextChannel, Thread, DMChannel]
	MessageableChannel = Union[PartialMessageableChannel, GroupChannel]
	SnowflakeTime = Union["Snowflake", datetime]

MISSING = utils.MISSING


class Mesle:
	"""An ABC that details the common operations on a model that can send messages.
    The following implement this ABC:
    - :class:`~discord.TextChannel`
    - :class:`~discord.DMChannel`
    - :class:`~discord.GroupChannel`
    - :class:`~discord.User`
    - :class:`~discord.Member`
    - :class:`~discord.ext.commands.Context`
    """

	__slots__ = ("_state","__get_l")
	_state: ConnectionState

	def __init__(self, state,s):
	  self._state, self.__get_l = state, s
	
	async def _get_channel(self) -> MessageableChannel:
		raise NotImplementedError

	@overload
	async def send(
	    self,
	    content: Optional[str] = ...,
	    *,
	    tts: bool = ...,
	    embed: Embed = ...,
	    file: File = ...,
	    delete_after: float = ...,
	    nonce: Union[str, int] = ...,
	    allowed_mentions: AllowedMentions = ...,
	    reference: Union[Message, MessageReference, PartialMessage] = ...,
	    mention_author: bool = ...,
	    view: View = ...,
	) -> Message:
		...

	@overload
	async def send(
	    self,
	    content: Optional[str] = ...,
	    *,
	    tts: bool = ...,
	    embed: Embed = ...,
	    files: List[File] = ...,
	    delete_after: float = ...,
	    nonce: Union[str, int] = ...,
	    allowed_mentions: AllowedMentions = ...,
	    reference: Union[Message, MessageReference, PartialMessage] = ...,
	    mention_author: bool = ...,
	    view: View = ...,
	) -> Message:
		...

	@overload
	async def send(
	    self,
	    content: Optional[str] = ...,
	    *,
	    tts: bool = ...,
	    embeds: List[Embed] = ...,
	    file: File = ...,
	    delete_after: float = ...,
	    nonce: Union[str, int] = ...,
	    allowed_mentions: AllowedMentions = ...,
	    reference: Union[Message, MessageReference, PartialMessage] = ...,
	    mention_author: bool = ...,
	    view: View = ...,
	) -> Message:
		...

	@overload
	async def send(
	    self,
	    content: Optional[str] = ...,
	    *,
	    tts: bool = ...,
	    embeds: List[Embed] = ...,
	    files: List[File] = ...,
	    delete_after: float = ...,
	    nonce: Union[str, int] = ...,
	    allowed_mentions: AllowedMentions = ...,
	    reference: Union[Message, MessageReference, PartialMessage] = ...,
	    mention_author: bool = ...,
	    view: View = ...,
	) -> Message:
		...

	async def send(
	    self,
	    content=None,
	    *,
	    tts=None,
	    embed=None,
	    embeds=None,
	    file=None,
	    files=None,
	    delete_after=None,
	    nonce=None,
	    allowed_mentions=None,
	    reference=None,
	    mention_author=None,
	    view=None,
	):
		"""|coro|
        Sends a message to the destination with the content given.
        The content must be a type that can convert to a string through ``str(content)``.
        If the content is set to ``None`` (the default), then the ``embed`` parameter must
        be provided.
        To upload a single file, the ``file`` parameter should be used with a
        single :class:`~discord.File` object. To upload multiple files, the ``files``
        parameter should be used with a :class:`list` of :class:`~discord.File` objects.
        **Specifying both parameters will lead to an exception**.
        To upload a single embed, the ``embed`` parameter should be used with a
        single :class:`~discord.Embed` object. To upload multiple embeds, the ``embeds``
        parameter should be used with a :class:`list` of :class:`~discord.Embed` objects.
        **Specifying both parameters will lead to an exception**.
        Parameters
        ------------
        content: Optional[:class:`str`]
            The content of the message to send.
        tts: :class:`bool`
            Indicates if the message should be sent using text-to-speech.
        embed: :class:`~discord.Embed`
            The rich embed for the content.
        file: :class:`~discord.File`
            The file to upload.
        files: List[:class:`~discord.File`]
            A list of files to upload. Must be a maximum of 10.
        nonce: :class:`int`
            The nonce to use for sending this message. If the message was successfully sent,
            then the message will have a nonce with this value.
        delete_after: :class:`float`
            If provided, the number of seconds to wait in the background
            before deleting the message we just sent. If the deletion fails,
            then it is silently ignored.
        allowed_mentions: :class:`~discord.AllowedMentions`
            Controls the mentions being processed in this message. If this is
            passed, then the object is merged with :attr:`~discord.Client.allowed_mentions`.
            The merging behaviour only overrides attributes that have been explicitly passed
            to the object, otherwise it uses the attributes set in :attr:`~discord.Client.allowed_mentions`.
            If no object is passed at all then the defaults given by :attr:`~discord.Client.allowed_mentions`
            are used instead.
            .. versionadded:: 1.4
        reference: Union[:class:`~discord.Message`, :class:`~discord.MessageReference`, :class:`~discord.PartialMessage`]
            A reference to the :class:`~discord.Message` to which you are replying, this can be created using
            :meth:`~discord.Message.to_reference` or passed directly as a :class:`~discord.Message`. You can control
            whether this mentions the author of the referenced message using the :attr:`~discord.AllowedMentions.replied_user`
            attribute of ``allowed_mentions`` or by setting ``mention_author``.
            .. versionadded:: 1.6
        mention_author: Optional[:class:`bool`]
            If set, overrides the :attr:`~discord.AllowedMentions.replied_user` attribute of ``allowed_mentions``.
            .. versionadded:: 1.6
        view: :class:`discord.ui.View`
            A Discord UI View to add to the message.
        embeds: List[:class:`~discord.Embed`]
            A list of embeds to upload. Must be a maximum of 10.
            .. versionadded:: 2.0
        Raises
        --------
        ~discord.HTTPException
            Sending the message failed.
        ~discord.Forbidden
            You do not have the proper permissions to send the message.
        ~discord.InvalidArgument
            The ``files`` list is not of the appropriate size,
            you specified both ``file`` and ``files``,
            or you specified both ``embed`` and ``embeds``,
            or the ``reference`` object is not a :class:`~discord.Message`,
            :class:`~discord.MessageReference` or :class:`~discord.PartialMessage`.
        Returns
        ---------
        :class:`~discord.Message`
            The message that was sent.
        """

		channel = self.__get_l
		state = self._state
		content = str(content) if content is not None else None

		if embed is not None and embeds is not None:
			raise InvalidArgument(
			    'cannot pass both embed and embeds parameter to send()')

		if embed is not None:
			embed = embed.to_dict()

		elif embeds is not None:
			if len(embeds) > 10:
				raise InvalidArgument(
				    'embeds parameter must be a list of up to 10 elements')
			embeds = [embed.to_dict() for embed in embeds]

		if allowed_mentions is not None:
			if state.allowed_mentions is not None:
				allowed_mentions = state.allowed_mentions.merge(
				    allowed_mentions).to_dict()
			else:
				allowed_mentions = allowed_mentions.to_dict()
		else:
			allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict(
			)

		if mention_author is not None:
			allowed_mentions = allowed_mentions or AllowedMentions().to_dict()
			allowed_mentions['replied_user'] = bool(mention_author)

		if reference is not None:
			try:
				reference = reference.to_message_reference_dict()
			except AttributeError:
				raise InvalidArgument(
				    'reference parameter must be Message, MessageReference, or PartialMessage'
				) from None

		if view:
			if not hasattr(view, '__discord_ui_view__'):
				raise InvalidArgument(
				    f'view parameter must be View not {view.__class__!r}')

			components = view.to_components()
		else:
			components = None

		if file is not None and files is not None:
			raise InvalidArgument(
			    'cannot pass both file and files parameter to send()')

		if file is not None:
			if not isinstance(file, File):
				raise InvalidArgument('file parameter must be File')

			try:
				data = await state.http.send_files(
				    channel.id,
				    files=[file],
				    allowed_mentions=allowed_mentions,
				    content=content,
				    tts=tts,
				    embed=embed,
				    embeds=embeds,
				    nonce=nonce,
				    message_reference=reference,
				    components=components,
				)
			finally:
				file.close()

		elif files is not None:
			if len(files) > 10:
				raise InvalidArgument(
				    'files parameter must be a list of up to 10 elements')
			elif not all(isinstance(file, File) for file in files):
				raise InvalidArgument('files parameter must be a list of File')

			try:
				data = await state.http.send_files(
				    channel.id,
				    files=files,
				    content=content,
				    tts=tts,
				    embed=embed,
				    embeds=embeds,
				    nonce=nonce,
				    allowed_mentions=allowed_mentions,
				    message_reference=reference,
				    components=components,
				)
			finally:
				for f in files:
					f.close()
		else:
			data = await state.http.send_message(
			    channel.id,
			    content,
			    tts=tts,
			    embed=embed,
			    embeds=embeds,
			    nonce=nonce,
			    allowed_mentions=allowed_mentions,
			    message_reference=reference,
			    components=components,
			)

		ret = state.create_message(channel=channel, data=data)
		if view:
			state.store_view(view, ret.id)

		if delete_after is not None:
			await ret.delete(delay=delete_after)
		return ret
