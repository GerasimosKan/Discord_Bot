const {Client, Attachment} = require("discord.js");
const bot = new Client();
const ytdl = require('ytdl-core');

//TOKEN GIA BOT
const token ="NTkwOTE4OTAzNzc4MjQ2NjU2.XQpnvA.XP-N5QBujlHi1tI_hqdTRNQoJJg";

//Start command
const PREFIX = "";

//Bot online
bot.on("ready", ()=> {
    console.log("BOT ONLINE");
});

//Wellcome message
bot.on('guildMemberAdd', member =>{
    const channel = member.guild.channels.find(channel => channel.name === "general");
    if (!channel) return;

    channel.send(`Όπα καλωσόρισες ΨΑΡΑΚΛΑ ${member} πάνε καθάρισε τις καλλιόπες`)
});

//Permition
bot.on('guildMemberAdd', function(member){
    let Role= member.guild.roles.find("name", "ROOKIE");
    member.addRole(Role);
});


//OPA FILE
bot.on("message", message=>{

    let args = message.content.substring(PREFIX.length).split(" ");

    switch(args[0]){
        case 'send':
                const filos = new Attachment('./1.png')
                message.channel.send(message.author, filos);
            break;
    }
})

//PROSEXE TI LES PITSIRIKO
bot.on("message", message=>{

    let args = message.content.substring(PREFIX.length).split(" ");

    switch(args[0]){
        case 'gamo':
                const filos = new Attachment('./2.png')
                message.channel.send(message.author, filos);
            break;
    }
})

//gay
bot.on("message", message=>{

    let args = message.content.substring(PREFIX.length).split(" ");

    switch(args[2]){
        case 'gay':
                message.channel.send("no u");
        break;
    }
})

//Fotoulis
bot.on('message', message => {
    // Voice only works in guilds, if the message does not come from a guild,
    // we ignore it
    if (!message.guild) return;
  
    if (message.content === 'fotoulis') {
      // Only try to join the sender's voice channel if they are in one themselves
      if (message.member.voiceChannel) {
        message.member.voiceChannel.join()
          .then(connection => { // Connection is an instance of VoiceConnection
            message.channel.send('!play https://www.youtube.com/watch?v=bbJHFD3UBYM');
          })
          .catch(console.log);
      } else {
        message.reply('You need to join a voice channel first!');
      }
    }
  });



bot.login(token);