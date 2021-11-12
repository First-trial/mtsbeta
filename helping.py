from discoutils import MinimalEmbedHelp as Meh

class Myh(Meh):
	def add_bot_commands_formatting(self, commands, heading):
		if commands:
			joined = ',\u2002'.join("`" + c.name + "`" for c in commands)
			self.paginator.add_line(f'__**{heading}**__')
			self.paginator.add_line(joined)

	def add_subcommand_formatting(self, command):
		fmt = '{0}{1} \N{EN DASH} `{2}`' if command.brief else '{0}{1} \N{EN DASH} `No description`'
		self.paginator.add_line(
		    fmt.format(self.context.clean_prefix, command.qualified_name,
		               command.short_doc))

My =Myh(color=0x00ffff)