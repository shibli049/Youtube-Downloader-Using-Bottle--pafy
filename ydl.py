#-------------------------------------------------------------------------------
# Name:        Youtube Downloader Using pafy and bottle
# Purpose:     Download Youtube videos in desired format including
#              (mp4,webm,3gp,flv etc) with details information.
# Author:      shovon
# Facebook:    https://www.facebook.com/ars.shovon
# Created:     08-04-2015
# Instruction: Open localhost:8080/download from browser after running the program
#-------------------------------------------------------------------------------

import pafy
from flask import Flask, render_template_string, url_for, redirect, request
import os
import logging

logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.debug = False
app.config.from_object(__name__)
TOKEN = str(os.environ.get('TOKEN', 'Test1234'))
print("TOKEN:", TOKEN)

def generate_youtube_link(passed_url):
    url=passed_url
    video = pafy.new(url)
    str_output='''
    <div class="well">
        <div class="media">
            <div class="media-left media-middle">
    '''
    thumb="<img class='media-object' src='"+video.thumb+"'/>";
    str_output=str_output+thumb+"</div><div class='media-body'>"
    title="<h4 class='media-heading'>Title: "+video.title+"</h4>"
    author="<b>Author: </b>"+video.author+"<br>"
    rating_str=str(round(video.rating,4))
    rating="<b>Rating: </b>"+rating_str
    view_count="<b>Total view: </b>"+str(video.viewcount)
    like="<b>Like: </b>" + str(video.likes)
    dislike="<b>Disike: </b>" + str(video.dislikes)
    duration="<b>Video duration: </b>"+str(video.duration)
    description="<p><b>Description: </b> " + video.description +"</p>" 
    str_output=str_output+title+author
    str_output=str_output+view_count+", "+duration+", "+like+", "+dislike+", "+rating
    str_output=str_output+description+"</div></div></div>"

    my_str="<h1>Video Links</h1><table class='table table-hover table-bordered table-striped'><tr><th>RESOLUTION</th><th>EXTENSION</th><th>FILESIZE</th><th>URL</th></tr>"
    streams=video.streams
    for s in streams:
        my_str=my_str+"<tr><td>"+s.resolution+"</td><td>"+s.extension+"</td><td>"+str(s.get_filesize()/1000)+" KB</td><td><a download href="+s.url+">Download link</a></td></tr>"

    str_output=str_output+my_str+"</table>"

    my_aud_str="<hr/><h1>Audio Links</h1><table class='table table-hover table-bordered table-striped'><tr><th>BITRATE</th><th>EXTENSION</th><th>FILESIZE</th><th>URL</th></tr>"
    streams=video.audiostreams
    for s in streams:
        my_aud_str=my_aud_str+"<tr><td>"+s.bitrate+"</td><td>"+s.extension+"</td><td>"+str(s.get_filesize()/1000)+" KB</td><td><a download href="+s.url+">Download link</a></td></tr>"
    str_output=str_output+my_aud_str+"</table>"


    return str_output

@app.route('/', methods=['GET'])
def index():

        str_header='''
        <html>
        	<head>
        		<title>YouTube Downloader</title>
        		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
        		<!-- Latest compiled and minified CSS -->
        		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
                <link rel="shortcut icon" href="http://mindberry.net/images/download.png">
        		<style type="text/css">
        			body{
        				margin: 20px auto;
        			}
                    .media-object{
        			  padding: 4px;
        			  background-color: #fff;
        			  border: 1px solid #ddd;
        			  border-radius: 4px;
        			}
                    #youtube_link{
                      width:550px;
                    }
        		</style>
        	</head>
        	<body>
        		<div class="container">
        '''
        str_footer='''
                </div>
        	</body>
        </html>
        '''
        str_form='''
    			<form class="form-inline" action="/" method="GET">
                    <label class="sr-only" for="youtube_link">YouTube Link:</label>
                    <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                        <div class="input-group-addon">YouTube Link:</div>
                        <input name="youtubelink" type="text" class="form-control" id="youtube_link" placeholder="Paste YouTube link Here.">
                    </div>
                    <label class="sr-only" for="token">Token</label>
                    <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                        <div class="input-group-addon">Token:</div>
                        <input type="text" class="form-control" id="token" name="token" placeholder="Your DL Token">
                    </div>
                    <button type="submit" class="btn btn-info" value="savebtn" name="savebtn" >Download Links</button>
                    <button onclick="window.location = window.location.pathname" type="button" class="btn btn-default"><span class="glyphicon glyphicon-repeat" aria-hidden="true"></span></button>
                </form>
        ''';
        # print("werwer" , request.args)
        if request.args.get('savebtn','').strip():
            youtubelink = request.args.get('youtubelink', '').strip()
            token = request.args.get('token', '').strip()
            # print(token, TOKEN)
            if(token != TOKEN):
                return render_template_string(str_header+str_form+str_footer)
            returned_str=generate_youtube_link(youtubelink)
            show_str=str_header+str_form+returned_str+str_footer
            return render_template_string((show_str))
        else:
            return render_template_string(str_header+str_form+str_footer)

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 8080))
    print("Open http://localhost:" + str(PORT) + "/ from browser")
    print(dir(request))
    app.run(host='0.0.0.0', port=PORT)
    
