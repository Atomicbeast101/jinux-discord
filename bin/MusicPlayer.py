from datetime import datetime, timedelta
from random import shuffle
from bin import yt_title
import re


def create_yt_url(_youtube_id):
    return 'https://www.youtube.com/watch?v={}'.format(_youtube_id)


def usage_msg(_cmd, _mention, _cmdchar):
    return ':warning: {} **USAGE:** {}{}'.format(_mention, _cmdchar, _cmd)


def get_youtube_id(_url):
    regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.'
                       r'(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
    match = regex.match(_url)
    if match:
        return match.group('id')
    return None


def name_exists(_db_ex, _name):
    for row in _db_ex.execute('SELECT name FROM playlist WHERE name=?;', (_name, )):
        return True
    return False


def song_exists(_db_ex, _youtube_id):
    for row in _db_ex.execute('SELECT name FROM song WHERE youtube_id=?;', (_youtube_id, )):
        return True
    return False


def song_exists_in_playlist(_db_ex, _name, _youtube_id):
    for row in _db_ex.execute('SELECT * FROM playlist_song WHERE name=? AND youtube_id=?;', (_name, _youtube_id)):
        return True
    return False


def name_valid(_name):
    if re.match('^[\w\d_-]*$', _name):
        return True
    return False


def has_permission(_db_ex, _name, _channel, _author):
    owner = ''
    for row in _db_ex.execute('SELECT owner FROM playlist WHERE name=?;', (_name, )):
        owner = row[0]
    if owner == _author.id:
        return True
    elif _channel.permissions_for(_author).administrator:
        return True
    return False


def announce_song(_status, _curr_song_duration, _curr_song_end, _curr_song_title):
    diff = _curr_song_duration - (_curr_song_end - datetime.now()).seconds
    diff_min, diff_sec = divmod(diff, 60)
    dur_min, dur_sec = divmod(_curr_song_duration, 60)
    if _status == 0:  # Not playing
        return '''**Song Paused:**
```markdown
[{}:{:02}/{}:{:02}]: {}```'''.format(diff_min, diff_sec, dur_min, dur_sec, _curr_song_title)
    elif _status == 1:  # Is playing
        return '''**Song Playing:**
```markdown
[{}:{:02}/{}:{:02}]: {}```'''.format(diff_min, diff_sec, dur_min, dur_sec, _curr_song_title)
    else:  # Playing next
        return '''**Playing Next Song:**
```markdown
[{}:{:02}/{}:{:02}]: {}```'''.format(diff_min, diff_sec, dur_min, dur_sec, _curr_song_title)


class YTSong:
    def __init__(self):
        self.youtube_id = None
        self.title = None

    def set(self, _youtube_id):
        valid, title = yt_title.get_yt_title(_youtube_id)
        if valid:
            self.youtube_id = _youtube_id
            self.title = title
            return True
        return False

    def full_set(self, _youtube_id, _title):
        self.youtube_id = _youtube_id
        self.title = _title

    def get_youtube(self):
        return create_yt_url(self.youtube_id)


class MusicPlayer:
    def __init__(self):
        self.dclient = None

        self.text_channel = None
        self.voice_channel = None
        self.voice_manager = None

        self.playing = False
        self.player = None

        self.curr_song = None
        self.curr_song_duration = -1
        self.curr_song_end = None
        self.queue_spot = -1
        self.song_queue = list()

        self.mus_playlistnamecharlimit = None

        self.cmdchar = None

        self.db = None
        self.db_ex = None

    async def set(self, _dclient, _text_channel, _voice_channel, _mus_playlistnamecharlimit, _cmdchar, _db, _db_ex):
        try:
            self.dclient = _dclient

            self.text_channel = _text_channel
            self.voice_channel = _voice_channel
            self.voice_manager = await self.dclient.join_voice_channel(self.voice_channel)

            self.mus_playlistnamecharlimit = _mus_playlistnamecharlimit
            self.cmdchar = _cmdchar

            self.db = _db
            self.db_ex = _db_ex

            return True
        except Exception:
            return False

    async def auto_switch_song(self):
        if self.playing:
            if self.player is not None:
                if self.player.is_done():
                    if len(self.song_queue) > 0:
                        self.queue_spot += 1
                        if self.queue_spot >= len(self.song_queue):
                            self.queue_spot = 0
                        self.player.stop()
                        self.curr_song = self.song_queue[self.queue_spot]
                        self.player = None
                        self.player = await self.voice_manager.create_ytdl_player(self.curr_song.get_youtube())
                        self.curr_song_duration = self.player.duration
                        self.curr_song_end = datetime.now() + timedelta(seconds=self.player.duration)
                        self.player.start()
                        await self.dclient.send_message(self.text_channel, announce_song(2, self.curr_song_duration,
                                                                                         self.curr_song_end,
                                                                                         self.curr_song.title))

    # -play, -play <youtube_url>
    async def play(self, _msg, _mention):
        _msg = _msg.split(' ')

        # -play
        if len(_msg) == 1:
            if self.playing:
                if self.player.is_playing():
                    await self.dclient.send_message(self.text_channel, ':warning: {} There\'s already a song playing '
                                                                       'right now!'.format(_mention))
                else:
                    if self.player.is_done():
                        if len(self.song_queue) > 0:
                            self.player.stop()
                            self.curr_song = self.song_queue[self.queue_spot]
                            self.player = None
                            self.player = await self.voice_manager.create_ytdl_player(self.curr_song.get_youtube())
                            self.curr_song_duration = self.player.duration
                            self.curr_song_end = datetime.now() + timedelta(seconds=self.player.duration)
                            self.player.start()
                            self.playing = True
                            await self.dclient.send_message(self.text_channel, announce_song(1, self.curr_song_duration,
                                                                                             self.curr_song_end,
                                                                                             self.curr_song.title))
                        else:
                            await self.dclient.send_message(self.text_channel,
                                                            ':warning: {} There\'s no queued songs to '
                                                            'play!'.format(_mention))
                    else:
                        self.player.resume()
                        await self.dclient.send_message(self.text_channel, announce_song(1, self.curr_song_duration,
                                                                                         self.curr_song_end,
                                                                                         self.curr_song.title))
            else:
                if len(self.song_queue) > 0:
                    self.curr_song = self.song_queue[self.queue_spot]
                    self.player = None
                    self.player = await self.voice_manager.create_ytdl_player(self.curr_song.get_youtube())
                    self.curr_song_duration = self.player.duration
                    self.curr_song_end = datetime.now() + timedelta(seconds=self.player.duration)
                    self.player.start()
                    self.playing = True
                    await self.dclient.send_message(self.text_channel, announce_song(1, self.curr_song_duration,
                                                                                     self.curr_song_end,
                                                                                     self.curr_song.title))
                else:
                    await self.dclient.send_message(self.text_channel, ':warning: {} There\'s no queued songs to '
                                                                       'play!'.format(_mention))

        # -play <youtube_url>
        elif len(_msg) == 2:
            youtube_id = get_youtube_id(_msg[1])
            if youtube_id is None:
                await self.dclient.send_message(self.text_channel, ':warning: {} Invalid YouTube URL!'.format(_mention))
            else:
                new_song = YTSong()
                if new_song.set(youtube_id):
                    if self.player is not None:
                        self.player.stop()
                    self.curr_song = new_song
                    self.player = None
                    self.player = await self.voice_manager.create_ytdl_player(self.curr_song.get_youtube())
                    self.curr_song_duration = self.player.duration
                    self.curr_song_end = datetime.now() + timedelta(seconds=self.player.duration)
                    self.player.start()
                    self.playing = True
                    await self.dclient.send_message(self.text_channel, announce_song(1, self.curr_song_duration,
                                                                                     self.curr_song_end,
                                                                                     self.curr_song.title))
                else:
                    await self.dclient.send_message(self.text_channel, ':warning: {} This YouTube video doesn\'t exist!'
                                                    .format(_mention))

        else:
            await self.dclient.send_message(self.text_channel, usage_msg('play <youtube_url>', _mention, self.cmdchar))

    # -playing
    async def play_status(self, _mention):
        if self.playing:
            if self.player.is_playing():
                await self.dclient.send_message(self.text_channel, announce_song(1, self.curr_song_duration,
                                                                                 self.curr_song_end,
                                                                                 self.curr_song.title))
            else:
                await self.dclient.send_message(self.text_channel, announce_song(0, self.curr_song_duration,
                                                                                 self.curr_song_end,
                                                                                 self.curr_song.title))
        else:
            await self.dclient.send_message(self.text_channel, ':warning: {} There\'s no song playing right now!'
                                            .format(_mention))

    # -pause
    async def pause(self, _mention):
        if self.playing:
            if self.player.is_playing():
                self.player.pause()
                await self.dclient.send_message(self.text_channel, ':pause_button: Current song paused!')
            else:
                await self.dclient.send_message(self.text_channel, ':warning: {} Current song already paused!'
                                                .format(_mention))
        else:
            await self.dclient.send_message(self.text_channel, ':warning: {} There\'s no song in play/pause mode right '
                                                               'now!'.format(_mention))

    # -stop
    async def stop(self, _mention):
        if self.playing:
            self.playing = False
            self.player.stop()
            self.player = None
            self.song_queue = list()
            self.queue_spot = -1
            self.curr_song = None
            self.curr_song_duration = None
            self.curr_song_end = None
            await self.dclient.send_message(self.text_channel, ':octagonal_sign: Current song has been stopped and '
                                                               'removed!')
        else:
            await self.dclient.send_message(self.text_channel, ':warning: {} There\'s no song in play/pause mode right '
                                                               'now!'.format(_mention))

    # -shuffle
    async def shuffle(self, _mention):
        if len(self.song_queue) > 2:
            if not self.playing:
                self.curr_song = self.song_queue[self.queue_spot]
            del self.song_queue[self.queue_spot]
            shuffle(self.song_queue)
            self.song_queue.insert(0, self.curr_song)
            self.queue_spot = 0
            await self.dclient.send_message(self.text_channel, 'Active playlist has been shuffled!')
        else:
            await self.dclient.send_message(self.text_channel, ':warning: {} Can\'t shuffle the queued list that isn\'t'
                                                               ' greater than 2!'.format(_mention))

    # -queue <youtube_url>
    async def queue(self, _msg, _mention):
        _msg = _msg.split(' ')
        if len(_msg) == 2:
            youtube_id = get_youtube_id(_msg[1])
            if youtube_id is None:
                await self.dclient.send_message(self.text_channel, ':warning: {} Invalid YouTube URL!')
            else:
                new_song = YTSong()
                if new_song.set(youtube_id):
                    self.song_queue.append(new_song)
                    await self.dclient.send_message(self.text_channel, '''**Next song in queue:**
```markdown
{}```'''.format(new_song.title))
                else:
                    await self.dclient.send_message(self.text_channel, ':warning: {} This YouTube video doesn\'t exist!'
                                                    .format(_mention))
        else:
            await self.dclient.send_message(self.text_channel, usage_msg('queue <youtube_url>', _mention, self.cmdchar))

    # -clear
    async def clear(self):
        if self.player is None:
            self.song_queue = list()
            await self.dclient.send_message(self.text_channel, 'Active playlist/queued list has been cleared!')
        else:
            self.song_queue = list()
            self.song_queue.append(self.curr_song)
            self.queue_spot = 0
            await self.dclient.send_message(self.text_channel, 'Active playlist/queued list has been cleared except for'
                                                               ' the current song in play/pause mode!')

    # -skip
    async def skip(self, _mention):
        if self.playing:
            if len(self.song_queue) > 1:
                if self.player.is_playing():
                    self.player.stop()
                self.queue_spot += 1
                if self.queue_spot >= len(self.song_queue):
                    self.queue_spot = 0
                self.curr_song = self.song_queue[self.queue_spot]
                self.player = None
                self.player = await self.voice_manager.create_ytdl_player(self.curr_song.get_youtube())
                self.curr_song_duration = self.player.duration
                self.curr_song_end = datetime.now() + timedelta(seconds=self.player.duration)
                self.player.start()
                await self.dclient.send_message(self.text_channel, announce_song(1, self.curr_song_duration,
                                                                                 self.curr_song_end,
                                                                                 self.curr_song.title))
            else:
                await self.dclient.send_message(self.text_channel, ':warning: {} There\'s only one song in the queued '
                                                                   'list!'.format(_mention))
        else:
            await self.dclient.send_message(self.text_channel, ':warning: {} There are no songs playing right now!'
                                            .format(_mention))

    # -volume <#>
    async def volume(self, _msg, _mention):
        _msg = _msg.split(' ')
        if len(_msg) == 2:
            try:
                level = int(_msg[1])
                if 0 <= level <= 200:
                    self.player.volume = level / 100.0
                    await self.dclient.send_message(self.text_channel, 'Volume has been set to `{}%`!'.format(level))
                await self.dclient.send_message(self.text_channel, ':warning: {} `{}` % value must be between `0` and '
                                                                   '`200`!'.format(_mention, level))
            except ValueError:
                await self.dclient.send_message(self.text_channel, ':warning: {} Invalid input! The value must be '
                                                                   'numeric.'.format(_mention))
        else:
            await self.dclient.send_message(self.text_channel, usage_msg('volume <#>', _mention, self.cmdchar))

    # -playlist, -playlist all, -playlist list <name>, -playlist create <name>, -playlist remove <name>,
    # -playlist edit <name> add <youtube_url>, -playlist edit <name> remove <youtube_id>, -playlist empty <name>,
    # -playlist load <name>
    async def playlist(self, _msg, _mention, _author):
        _msg = _msg.split(' ')
        # -playlist
        if len(_msg) == 1:
            if len(self.song_queue) > 0:
                response = '''**Active Playlist/Queued List:**
```css
'''
                count = 0
                for song in self.song_queue:
                    if count == self.queue_spot:
                        response += '''> {:5} {}
'''.format('[' + str(count + 1) + ']:', song.title)
                    else:
                        response += '''  {:5} {}
'''.format('[' + str(count + 1) + ']:', song.title)
                    count += 1
                response += '''```'''
                await self.dclient.send_message(self.text_channel, response)
            else:
                await self.dclient.send_message(self.text_channel, ':warning: {} There are no songs in the active '
                                                                   'playlist/queued list!'.format(_mention))

        else:
            # -playlist all
            if _msg[1].lower() == 'all':
                names = list()
                for row in self.db_ex.execute('SELECT name FROM playlist;'):
                    names.append(row[0])
                if len(names) > 0:
                    await self.dclient.send_message(self.text_channel, '''**List of Playlists:**
```{}```'''.format(', '.join(names)))
                else:
                    await self.dclient.send_message(self.text_channel, ':warning: {} There\'s no playlists made!'
                                                    .format(_mention))

            # -playlist list <name>
            elif _msg[1].lower() == 'list':
                if len(_msg) == 3:
                    name = _msg[2].lower()
                    if name_exists(self.db_ex, name):
                        songs = {}
                        for row in self.db_ex.execute('SELECT song.youtube_id, song.name FROM song JOIN playlist_song '
                                                      'ON song.youtube_id=playlist_song.youtube_id AND '
                                                      'playlist_song.name=?;', (name, )):
                            songs[row[0]] = row[1]
                        if len(songs) > 0:
                            response = '''**Playlist `{}`:**
```css
'''.format(name)
                            for youtube_id, title in songs.items():
                                response += '''{:13} {}
'''.format('[' + youtube_id + ']:', title)
                            response += '''```'''
                            await self.dclient.send_message(self.text_channel, response)
                        else:
                            await self.dclient.send_message(self.text_channel, ':warning: {} Playlist `{}` is empty!'
                                                            .format(_mention, name))
                    else:
                        await self.dclient.send_message(self.text_channel, ':warning: {} Playlist `{}` doesn\'t exist!'
                                                        .format(_mention, name))
                else:
                    await self.dclient.send_message(self.text_channel, usage_msg('playlist list <name>', _mention,
                                                                                 self.cmdchar))

            # -playlist load <name>
            elif _msg[1].lower() == 'load':
                if len(_msg) == 3:
                    name = _msg[2].lower()
                    if name_exists(self.db_ex, name):
                        songs = {}
                        for row in self.db_ex.execute('SELECT song.youtube_id, song.name FROM song JOIN playlist_song '
                                                      'ON song.youtube_id=playlist_song.youtube_id AND '
                                                      'playlist_song.name=?;', (name,)):
                            songs[row[0]] = row[1]
                        if len(songs) > 0:
                            self.song_queue = list()
                            for youtube_id, title in songs.items():
                                song = YTSong()
                                song.full_set(youtube_id, title)
                                self.song_queue.append(song)
                            self.queue_spot = 0
                            if self.player is not None:
                                self.player.stop()
                            self.curr_song = self.song_queue[self.queue_spot]
                            self.player = await self.voice_manager.create_ytdl_player(self.curr_song.get_youtube())
                            self.curr_song_duration = self.player.duration
                            self.curr_song_end = datetime.now() + timedelta(seconds=self.player.duration)
                            self.player.start()
                            self.playing = True
                            await self.dclient.send_message(self.text_channel, 'Playlist `{}` has been loaded!'
                                                            .format(name))
                            await self.dclient.send_message(self.text_channel, announce_song(1, self.curr_song_duration,
                                                                                             self.curr_song_end,
                                                                                             self.curr_song.title))
                        else:
                            await self.dclient.send_message(self.text_channel, ':warning: {} Playlist `{}` is empty!'
                                                            .format(_mention, name))
                    else:
                        await self.dclient.send_message(self.text_channel, ':warning: {} Playlist `{}` doesn\'t exist!'
                                                        .format(_mention, name))
                else:
                    await self.dclient.send_message(self.text_channel, usage_msg('playlist load <name>', _mention,
                                                                                 self.cmdchar))

            # -playlist create <name>
            elif _msg[1].lower() == 'create':
                if len(_msg) == 3:
                    name = _msg[2].lower()
                    if name_exists(self.db_ex, name):
                        await self.dclient.send_message(self.text_channel, ':warning: {} Playlist `{}` already exists!'
                                                        .format(_mention, name))
                    else:
                        if len(name) > 50:
                            await self.dclient.send_message(self.text_channel, ':warning: {} Name `{}` must be less '
                                                                               'than `50` characters!'.format(_mention,
                                                                                                              name))
                        else:
                            if len(name) <= self.mus_playlistnamecharlimit:
                                if name_valid(name):
                                    self.db_ex.execute('INSERT INTO playlist VALUES (?, ?);', (name, _author.id))
                                    self.db.commit()
                                    await self.dclient.send_message(self.text_channel, 'Playlist `{}` has been created!'
                                                                    .format(name))
                                else:
                                    await self.dclient.send_message(self.text_channel,
                                                                    ':warning: {} Playlist names can only contain any '
                                                                    '`numbers`, `letters`, and `_` & `-`. '
                                                                    .format(_mention))
                            else:
                                await self.dclient.send_message(self.text_channel, ':warning: {} Name `{}` must be less'
                                                                                   ' than `{}` characters!'
                                                                .format(_mention, name, self.mus_playlistnamecharlimit))
                else:
                    await self.dclient.send_message(self.text_channel, usage_msg('playlist create <name>', _mention,
                                                                                 self.cmdchar))

            # -playlist remove <name>
            elif _msg[1].lower() == 'remove':
                if len(_msg) == 3:
                    name = _msg[2].lower()
                    if name_exists(self.db_ex, name):
                        if name_exists(self.db_ex, name):
                            # TODO use transaction
                            self.db_ex.execute('DELETE FROM playlist_song WHERE name=?;', (name, ))
                            self.db_ex.execute('DELETE FROM playlist WHERE name=? AND owner=?', (name, _author.id))
                            self.db.commit()
                            await self.dclient.send_message(self.text_channel, 'Playlist `{}` has been removed!'.format(name))
                        else:
                            await self.dclient.send_message(self.text_channel, ':warning: {} Playlist `{}` doesn\'t '
                                                                               'exist!'.format(_mention, name))
                else:
                    await self.dclient.send_message(self.text_channel, usage_msg('playlist remove <name>', _mention,
                                                                                 self.cmdchar))

            # -playlist empty <name>
            elif _msg[1].lower() == 'empty':
                if len(_msg) == 3:
                    name = _msg[2].lower()
                    if name_exists(self.db_ex, name):
                        if name_exists(self.db_ex, name):
                            if has_permission(self.db_ex, name, self.text_channel, _author):
                                self.db_ex.execute('DELETE FROM playlist_song WHERE name=?;', (name, ))
                                self.db.commit()
                                await self.dclient.send_message(self.text_channel, 'Playlist `{}` has been emptied!'
                                                                .format(name))
                            else:
                                await self.dclient.send_message(self.text_channel, ':warning: {} You do not own `{}` '
                                                                                   'playlist!'.format(_mention, name))
                        else:
                            await self.dclient.send_message(self.text_channel, ':warning: {} Playlist `{}` doesn\'t '
                                                                               'exist!'.format(_mention, name))
                else:
                    await self.dclient.send_message(self.text_channel, usage_msg('playlist empty <name>', _mention,
                                                                                 self.cmdchar))

            # -playlist edit <name> add <youtube_url>
            # -playlist edit <name> remove <youtube_id>
            elif _msg[1].lower() == 'edit':
                if len(_msg) == 5:
                    name = _msg[2].lower()
                    if name_exists(self.db_ex, name):
                        if name_exists(self.db_ex, name):
                            if has_permission(self.db_ex, name, self.text_channel, _author):
                                # -playlist edit <name> add <youtube_url>
                                if _msg[3].lower() == 'add':
                                    youtube_id = get_youtube_id(_msg[4])
                                    if youtube_id is None:
                                        await self.dclient.send_message(self.text_channel,
                                                                        ':warning: {} Invalid YouTube URL!')
                                    else:
                                        song = YTSong()
                                        if song.set(youtube_id):
                                            if not song_exists(self.db_ex, youtube_id):
                                                self.db_ex.execute('INSERT INTO song VALUES (?, ?);', (youtube_id,
                                                                                                       song.title))
                                                self.db.commit()
                                            if song_exists_in_playlist(self.db_ex, name, youtube_id):
                                                await self.dclient.send_message(self.text_channel,
                                                                                ':warning: {} Song `{}` already exists '
                                                                                'in the `{}` playlist!'
                                                                                .format(_mention, name, song.title))
                                            else:
                                                self.db_ex.execute('INSERT INTO playlist_song VALUES (?, ?);',
                                                                   (name, youtube_id))
                                                self.db.commit()
                                                await self.dclient.send_message(self.text_channel,
                                                                                'Song `{}` has been added to `{}` '
                                                                                'playlist!'.format(song.title, name))
                                        else:
                                            await self.dclient.send_message(self.text_channel,
                                                                            ':warning: {} This YouTube video doesn\'t '
                                                                            'exist!'.format(_mention))

                                # -playlist edit <name> remove <youtube_id>
                                elif _msg[3].lower() == 'remove':
                                    youtube_id = _msg[4]
                                    if song_exists_in_playlist(self.db_ex, name, youtube_id):
                                        self.db_ex.execute()
                                        self.db.commit()
                                        valid, title = yt_title.get_yt_title(youtube_id)
                                        await self.dclient.send_message(self.text_channel,
                                                                        'Song `{}` has been removed from `{}` playlist!'
                                                                        .format(title, name))
                                    else:
                                        await self.dclient.send_message(self.text_channel,
                                                                        ':warning: {} YouTube ID `{}` doesn\'t exist in'
                                                                        ' `{}` playlist!'.format(_mention, youtube_id,
                                                                                                 name))

                                else:
                                    await self.dclient.send_message(self.text_channel,
                                                                    usage_msg('playlist edit <name> <add|remove> '
                                                                              '<youtube_url|youtube_id>', _mention,
                                                                              self.cmdchar))
                            else:
                                await self.dclient.send_message(self.text_channel, ':warning: {} You do not own `{}` '
                                                                                   'playlist!'.format(_mention, name))
                        else:
                            await self.dclient.send_message(self.text_channel, ':warning: {} Playlist `{}` doesn\'t '
                                                                               'exist!'.format(_mention, name))
                else:
                    await self.dclient.send_message(self.text_channel, usage_msg('playlist edit <name> <add|remove> '
                                                                                 '<youtube_url|youtube_id>', _mention,
                                                                                 self.cmdchar))

            else:
                await self.dclient.send_message(self.text_channel, usage_msg(
                    'playlist <all|list|load|create|remove|edit>', _mention, self.cmdchar))
