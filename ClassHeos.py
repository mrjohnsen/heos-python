import json
import telnetlib

class DenonDevice(object):
    """Representation of a Denon device."""

    def __init__(self, host):
        """Initialize the Denon device."""
        self._host = host
        self.heosurl = 'heos://player/'
        self.pid = ''

    def telnet_command(self, command):
        """Establish a telnet connection and sends `command`."""
        command = self.heosurl + command
        telnet = telnetlib.Telnet(self._host,1255)
        telnet.write(command.encode('ASCII') + b'\r\n')
        telnet.read_very_eager()  # skip response
        telnet.close()

    def telnet_request(self, command):
        """Execute `command` and return the response."""
        telnet = telnetlib.Telnet(self._host,1255)
        command = self.heosurl + command
        telnet.write(command.encode('ASCII') + b'\r\n')
        response = ''
        while True:
            response += telnet.read_some().decode()
            try:
                response = json.loads(response)
                break
            except ValueError:
                pass
        return response

    def name(self):
        """Return the name of the device."""
        name = self.telnet_request('get_player_info?pid={0}'.format(self.pid))
        return name['payload']['name']

    def source(self):
        """Return the current input source."""
        media_title = self.telnet_request('get_now_playing_media?pid={0}'.format(self.pid))
        return media_title['payload']['type'] 

    def media_title(self):
        """Current media info."""
        media_title = self.telnet_request('get_now_playing_media?pid={0}'.format(self.pid))
        return media_title['payload']['station'] 
    
    def volume_up(self):
        """Volume up media player."""
        self.telnet_command('volume_up?pid={0}'.format(self.pid))

    def volume_down(self):
        """Volume down media player."""
        self.telnet_command('volume_down?pid={0}'.format(self.pid))

    def media_play(self):
        """Play media media player."""
        self.telnet_command('set_play_state?pid={0}&state=play'.format(self.pid))

    def media_pause(self):
        """Pause media player."""
        self.telnet_command('set_play_state?pid={0}&state=pause'.format(self.pid))
        
    def media_stop(self):
        """Stop media media player."""
        self.telnet_command('set_play_state?pid={0}&state=stop'.format(self.pid))

