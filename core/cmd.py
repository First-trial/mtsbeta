class Command:
	bot = None
	name = "CommandName"
	help = "CommandHelp"
	brief = "CommandBrief"
	args = "CommandArgs"
	category = "CommandCategory"

	@classmethod
	def add_command(cls, bot):
		cls.bot = bot
		cls.bot.remove_command(cls.name)
		alias = []
		if hasattr(cls, "aliases"):
			alias = cls.aliases
		kwargs = {"aliases": alias}
		cmd = cls.bot.command(name=cls.name,
		                      brief=cls.brief,
		                      usage=cls.args,
		                      **kwargs)(cls.handler)
		cmd.cog = cls.bot.get_cog("Games")
		new_list = [cmd]
		for cmd in bot.get_cog("Games").__cog_commands__:
			new_list.append(cmd)
		bot.get_cog("Games").__cog_commands__ = new_list

	@classmethod
	async def handler(cls, self, context):
		missing_permissions = cls.bot.get_missing_permissions(context)
		if len(missing_permissions) > 0:
			await cls.bot.send_missing_permissions(context,
			                                       missing_permissions)
			return

		await cls.invoke(context)

	@classmethod
	async def invoke(cls, context):
		pass

	@classmethod
	def has_permission(cls, user_id):
		return True
