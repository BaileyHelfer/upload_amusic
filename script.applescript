on run argv
    -- Check if enough arguments are passed
    if (count of argv) < 5 then
        display dialog "Usage: osascript script.scpt <songFilePath> <newArtistName> <newAlbumName> <songName> <artworkFilePath>"
        return
    end if

    -- Debugging: Display the arguments passed
    display dialog "Arguments passed: " & (item 1 of argv) & ", " & (item 2 of argv) & ", " & (item 3 of argv) & ", " & (item 4 of argv) & ", " & (item 5 of argv)

    -- Retrieve the arguments
    set songFilePath to POSIX file (item 1 of argv)
    set newArtistName to item 2 of argv
    set newAlbumName to item 3 of argv
    set songName to item 4 of argv
    set artworkFilePath to POSIX file (item 5 of argv)

    -- Debugging: Display the file paths and names
    -- display dialog "Song File Path: " & (item 1 of argv)
    -- display dialog "Artwork File Path: " & (item 5 of argv)
    -- display dialog "Artist Name: " & newArtistName
    -- display dialog "Album Name: " & newAlbumName
    -- display dialog "Song Name: " & songName

    -- Add the song to the library
    tell application "Music"
        try
            set newTrack to add songFilePath to library playlist 1
            -- display dialog "Song added successfully."

            -- Set the artist, album name, and song name
            try
                set artist of newTrack to newArtistName
                -- display dialog "Artist set successfully: " & newArtistName
            on error errMsg number errNum
                -- display dialog "Error setting artist: " & errMsg & " (" & errNum & ")"
            end try

            try
                set album of newTrack to newAlbumName
                -- display dialog "Album set successfully: " & newAlbumName
            on error errMsg number errNum
                -- display dialog "Error setting album: " & errMsg & " (" & errNum & ")"
            end try

            try
                set name of newTrack to songName
                -- display dialog "Song name set successfully: " & songName
            on error errMsg number errNum
                -- display dialog "Error setting song name: " & errMsg & " (" & errNum & ")"
            end try

            -- Add artwork if provided
            if artworkFilePath is not "" then
                try
                    set artworkData to read artworkFilePath as «class PNGf»
                    set data of artwork 1 of newTrack to artworkData
                    -- display dialog "Artwork added successfully."
                on error errMsg number errNum
                    -- display dialog "Error adding artwork: " & errMsg & " (" & errNum & ")"
                end try
            end if
        on error errMsg number errNum
            -- display dialog "Error adding song to library: " & errMsg & " (" & errNum & ")"
        end try
    end tell
end run
