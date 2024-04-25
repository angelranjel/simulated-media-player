from media import Media, Track, Movie
from linked_list import LinkedList
import json
class Player:
    """
    A media player class that manages a playlist of media.

    This class utilizes a doubly linked list (LinkedList) to store and manage media in a playlist.
    It provides methods for adding, removing, playing, and navigating through media.

    Attributes
    ----------
    playlist : LinkedList
        A doubly linked list that stores the media in the playlist.
    currentMediaNode : Node or None
        The current media being played, represented as a node in the linked list.
    """

    def __init__(self):
        """
        Initializes the Player with an empty playlist and None as currentMediaNode.
        """
        self.playlist = LinkedList()
        self.currentMediaNode = None

    def addMedia(self, media):
        """
        Adds a media to the end of the playlist.
        Set the currentMediaNode to the first node in the playlist, 
        if currentMediaNode is None. 

        Parameters
        ----------
        media : Media | Track | Movie 
            The media to add to the playlist.
        """
        self.playlist.append(media)
        if not self.currentMediaNode:
            self.currentMediaNode = self.playlist.dummyHead.next

    def removeMedia(self, index) -> bool:
        """
        Removes a media from the playlist based on its index.
        You can assume the only invalid input is invalid index.
        Set the currentMediaNode to its next, if currentMediaNode is removed,
        and remeber using _isNodeUnbound(self.currentMediaNode) to check if a link is broken.

        Parameters
        ----------
        index : int
            The index of the media to remove.

        Returns
        -------
        bool
            True if the media was successfully removed, False otherwise.
        """
        if index < 0 or index >= self.playlist.size:
            return False

        current = self.playlist.dummyHead.next
        for i in range(index):
            current = current.next

        if self.currentMediaNode == current:
            self.currentMediaNode = current.next if current.next != self.playlist.dummyTail else None

        current.prev.next = current.next
        current.next.prev = current.prev
        self.playlist.size -= 1

        return True


    def next(self) -> bool:
        """
        Moves currentMediaNode to the next media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the next media, False otherwise.
        """
        if self.currentMediaNode and self.currentMediaNode.next != self.playlist.dummyTail:
            self.currentMediaNode = self.currentMediaNode.next
            return True
        return False

    def prev(self) -> bool:
        """
        Moves currentMediaNode to the previous media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the previous media, False otherwise.
        """
        if self.currentMediaNode and self.currentMediaNode.prev != self.playlist.dummyHead:
            self.currentMediaNode = self.currentMediaNode.prev
            return True
        return False

    def resetCurrentMediaNode(self) -> bool:
        """
        Resets the current media to the first media in the playlist,
        if the playlist contains at least one media. 

        Returns
        -------
        bool
            True if the current media was successfully reset, False otherwise.
        """
        if self.playlist.size > 0:
            self.currentMediaNode = self.playlist.dummyHead.next
            return True
        return False

    def play(self):
        """
        Plays the current media in the playlist. 
        Call the play method of the media instance.
        Remeber currentMediaNode is a node not a media, but its data is the actual
        media. If the currentMediaNode is None or its data is None, 
        print "The current media is empty.". 
        """
        if self.currentMediaNode and self.currentMediaNode.data:
            self.currentMediaNode.data.play()
        else:
            print("The current media is empty.")

    def playForward(self):
        """
        Plays all the media in the playlist from front to the end,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print "Playlist is empty.". 
        """
        if self.playlist.size == 0:
            print("Playlist is empty.")
        else:
            current = self.playlist.dummyHead.next
            while current != self.playlist.dummyTail:
                current.data.play()
                current = current.next

    def playBackward(self):
        """
        Plays all the media in the playlist from the back to front,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print this string "Playlist is empty.". 
        """
        if self.playlist.size == 0:
            print("Playlist is empty.")
        else:
            current = self.playlist.dummyTail.prev
            while current != self.playlist.dummyHead:
                current.data.play()
                current = current.prev

    def loadFromJson(self, fileName):
        """
        Loads media from a JSON file and adds them to the playlist.
        The order should be the same as the provided json file. 
        You could assume the filename is always valid
        Notice, for each given json object, 
        you should create instance of the correct instance type, (movie,track,media).
        You need to observe the provided json and figure how to do it.
        You could assume if a json object is not track or movie,
        it has to be a media.
        Pay attention the name of the key in each json object. 
        Set the currentMediaNode to the first media in the playlist, 
        if there is at least one media in the playlist.
        Remeber to use the dictionary get method. 

        Parameters
        ----------
        filename : str
            The name of the JSON file to load media from.
        """
        with open(fileName, 'r') as file:
            data = json.load(file)
            for item in data:
                media = Media(
                    title=item.get('collectionName'),
                    artist=item.get('artistName'),
                    releaseDate=item.get('releaseDate'),
                    url=item.get('collectionViewUrl')
                )
                
                if item.get('wrapperType') == 'track':
                    if item.get('kind') == 'feature-movie':
                        media = Movie(
                            title=item.get('trackName', 'No Title'),
                            artist=item.get('artistName', 'No Artist'),
                            releaseDate=item.get('releaseDate', 'No Release Date'),
                            url=item.get('trackViewUrl', 'No URL'),
                            rating=item.get('contentAdvisoryRating', 'No Rating'),
                            movieLength=item.get('trackTimeMillis', 0)
                        )
                    elif item.get('kind') == 'song':
                        media = Track(
                            title=item.get('trackName', 'No Title'),
                            artist=item.get('artistName', 'No Artist'),
                            releaseDate=item.get('releaseDate', 'No Release Date'),
                            url=item.get('trackViewUrl', 'No URL'),
                            album=item.get('collectionName', 'No Album'),
                            genre=item.get('primaryGenreName', 'No Genre'),
                            duration=item.get('trackTimeMillis', 0)
                        )

                self.addMedia(media)

        if self.playlist.size > 0:
            self.resetCurrentMediaNode()
