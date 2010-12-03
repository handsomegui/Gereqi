#Copyright 2009 Jonathan.W.Noble <jonnobleuk@gmail.com>

# This file is part of Gereqi.
#
# Gereqi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gereqi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gereqi.  If not, see <http://www.gnu.org/licenses/>.

import lastfm

class LastFm:
    def __init__(self):
        api_key = '588c694a81715cc12a4892d11b39d4db'
        secret = '39b99b7e1e4c446f69f3a52af126fe6'
        api = lastfm.Api(api_key)
        user = api.get_user("regomodo")
        top_artists = user.top_artists
        for art in top_artists:
            print art
        
LastFm()
