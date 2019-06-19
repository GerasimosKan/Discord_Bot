const {Client, Attachment} = require("discord.js");
const bot = new Client();

//TOKEN GIA BOT
const token ="NTkwOTE4OTAzNzc4MjQ2NjU2.XQpnvA.XP-N5QBujlHi1tI_hqdTRNQoJJg";
bot.login(token);

//Start command
const PREFIX = "!";

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

    switch(args[1]){
        case 'gamo tin mana sou':
                const filos = new Attachment('./2.png')
                message.channel.send(message.author, filos);
            break;
    }
})