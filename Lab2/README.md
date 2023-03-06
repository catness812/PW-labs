# How to use the `go2web` CLI?

:arrow_right: Run the executable. You'll be met with a lovely message.

:arrow_right: Make sure to first check the available commands by running `go2web -h`.

:arrow_right: If you want to make an HTTP request, follow the syntax `go2web -u <URL>`, replacing `<URL>` with your desired website. JSON data is accepted as well. If you happen to make a request to a resource that has been moved, worry not, HTTP request redirects are implemented.

:arrow_right: If you want to search something, just type `go2web -s <search-term>` and replace `<search-term>` with whatever it is you wanna search. Side note, multiple terms search is implemented, so you can enter as many terms as you wish after `-s`. Once the search is done, the CLI will prompt you with a choice whether or not you'd like to access any of the given resources.

:arrow_right: In order to save your precious time, the CLI will save the responses you get during a session and if you choose to navigate to a previous resource, it will let you know that it's printing the response out of cache memory.

:arrow_right: If you need to nagivate through previous commands, just use the up & down keys.

:arrow_right: Do not fret if you enter more spaces in between the keywords, the CLI will forgive you and give you the desired response.

:arrow_right: Lastly, if you're ready to part ways with `go2web`, enter `q`. The CLI will earnestly wait for your return.
