# DiscordBot_PostGraphs
A discord bot made to show graphs of a specific servers users post counts.

### Commands
* !graph pie - displays a pie diagram of total posts made by everyone on the server.
* !graph bar - displays a bar diagram of total posts made by everyone on the server.
* Optional command - An integer can follow after a whitespace to specify the max number of users to appear in the graph in the following manner: !graph bar 10

### Installation
Write the token associated with your bot in the conf file on the first line.
The following permissions are needed:
* View Channels
* Send Messages
* Attach Files
* Read Message History

##### Note
If there are channels that require specific permissions to be seen the bot will need those permissions as well, otherwise it will get request denied when trying to look at the past messages of said channel.

###### Token secrecy: Keep in mind that the token of your bot is secret. The token that can be seen in the commit log is invalid and served as an example at an earlier stage in the development. 
