import discord
import os
import youtube_dl
import ffmpeg

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

ffmpeg_options = {'options': "-vn"}
ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
              }],
        }
queue = []
title = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() in ['hi', 'hey', 'hello', 'hi bot']:
        await message.channel.send('Hello there! Wanna Groove with some Music?')

    elif message.content.startswith('$info'):
        await message.channel.send('```[info]```Hello, I am **Neuron-X**, a cutting-edge AI-powered bot currently undergoing development. I have been designed to effectively interact with users, answer their queries, and provide various services. For more information on Neuron-X, please feel free to contact my creator or visit our website at [*craft-x.vercel.app*](https://craft-x.vercel.com). Thank you for your interest in Neuron-X.')

    elif message.content.startswith('$help'):
        await message.channel.send('Here are a list of commands I support:\n ``` hey,hi,hello - greet the bot \n$info - get information about the bot \n$help - view this list of commands \n$play [song name] - play a song \n$next - play the next song in the queue \n$stop - stop the current song and clear the queue \n$pause - Pause the current song \n$resume - Resume the current song ```')

    elif message.content.startswith('$play'):
        voice_channel = message.author.voice.channel
        if voice_channel is None:
            await message.channel.send('You are not connected to any voice channel.')
            return
        song_name = message.content[5:]
        search_term = "ytsearch: " + song_name + ' song'
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(search_term, download=False)
            best_result = search_results['entries'][0]
            best_url = best_result['formats'][0]['url']
            queue.append(best_url)
            title.append(best_result['title'])
        if client.voice_clients:
            await message.channel.send(f'Song added to queue: ***{best_result["title"]}*** \n *{best_result["webpage_url"]}*')
        else:
            vc = await voice_channel.connect()
            source = discord.FFmpegOpusAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe", source= queue.pop(0))
            vc.play(source)
            await message.channel.send(f'Playing: ***{title.pop(0)}***  \n *{best_result["webpage_url"]}*')


    elif message.content.startswith('$next'):
        if client.voice_clients and queue:
            vc = client.voice_clients[0]
            vc.stop()
            source = discord.FFmpegOpusAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe", source= queue.pop(0))
            vc.play(source)
            await message.channel.send(f'Playing next song: ***{title.pop(0)}***')
        elif not queue:
            await message.channel.send('Queue is empty, add songs to play.')
        else:
            await message.channel.send('Bot is not connected to any voice channel.')


    elif message.content.startswith('$stop'):
        if client.voice_clients:
            vc = client.voice_clients[0]
            vc.stop()
            await vc.disconnect()
            queue.clear()
            await message.channel.send('Music Streaming stopped and queue cleared.')
        else:
            await message.channel.send('Bot is not connected to any voice channel.')


    elif message.content.startswith('$pause'):
        if message.author.voice is not None:
            voice_client = message.guild.voice_client
            if voice_client is not None:
                voice_client.pause()
                await message.channel.send('Music Streaming is Paused.')
            else:
                await message.channel.send('Not connected to a voice channel.')
        else:
            await message.channel.send('You are not connected to a voice channel.')


    elif message.content.startswith('$resume'):
        if message.author.voice is not None:
            voice_client = message.guild.voice_client
            if voice_client is not None:
                voice_client.resume()
                await message.channel.send('Music Streaming is Resumed.')
            else:
                await message.channel.send('Not connected to a voice channel.')
        else:
            await message.channel.send('You are not connected to a voice channel.')

client.run('ODA3MjQ2OTU5NTAwNTkxMTY0.YB1NUQ.LZM2mOjao84AGOpF22kLVcu63Jo')

