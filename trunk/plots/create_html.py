#!/usr/bin/env python
"""
Module to create a html file that lists all the png images in the current
folder.
The heml file is stored as HTML_FILE as given below
"""
import os
HTML_FILE = 'auto_html.html'

def create_html(plot_dir='.'):
    "Function to create the html page that shows the graphs"
    path = plot_dir
    dlist = os.listdir(path)
    dlist.sort()
    href_list = []
    date_list = []
    for dir_file in dlist:
        if dir_file.endswith('.png') and os.path.getsize(dir_file) > 0:
            try:
                href_list.append('<li /><a href="' + dir_file + '">' +
                                 dir_file + '</a><br> \n')
                date_list.append(str(dir_file).split('.')[1] + " " +
                                 str(dir_file).split('.')[2].replace('_', ':'))
            except IndexError:
                print "Timestamp format not recognized.",dir_file
    html_file = open(HTML_FILE,'w')
    table_contents = ''
    html_file.write ( """
    <html>
    <head>
    <center>
        <title>Pytomo: Youtube Download Statistics</title>
        <link type="text/css" rel="stylesheet" href="style.css" />
    </head>
    <body>
        <div id="nav"><div id="menu">
        <h1> Pytomo Statistics</h1>
        <ul>\n
        <table border="2" bgcolor = "#FF8C00" CELLPADDING="2" CELLSPACING="2
                     WIDTH="50%">
        <tr>
        <th width="150">Date Time </th>
        <th>File</th>
        </tr>             """)
    for i, line in enumerate(href_list):
        table_contents = table_contents + """
        <tr>
        <td><li />""" +  date_list[i] + """<br> </td>
        <td>""" + line + """</td>""" + """
        </tr>"""
    html_file.write(table_contents)
    html_file.write("""</table>
     <br/>
        </ul>
        </div></div>
    </center>
    </body>
    </html>   """)

if __name__ == '__main__':
    create_html()
