"""
Analyzing and reacting events related to server
"""

from mcdr.info import InfoSource
from mcdr.plugin.plugin_event import PluginEvents
from mcdr.reactor.abstract_reactor import AbstractReactor


class ServerReactor(AbstractReactor):
	def react(self, info):
		if info.source == InfoSource.SERVER:
			parser = self.server.parser_manager.get_parser()

			if parser.parse_server_startup_done(info):
				self.server.logger.debug('Server startup detected')
				self.server.flag_server_startup = True
				self.server.plugin_manager.dispatch_event(PluginEvents.SERVER_STARTUP, (self.server.server_interface,))

			if parser.parse_rcon_started(info):
				self.server.logger.debug('Server rcon started detected')
				self.server.flag_server_rcon_ready = True
				self.server.connect_rcon()

			if parser.parse_server_stopping(info):
				self.server.logger.debug('Server stopping detected')
				self.server.rcon_manager.disconnect()


def get_reactor(server):
	return ServerReactor(server)
