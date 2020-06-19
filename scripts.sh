python3 editor.py routine --video ../synfig/christmas_visuals.mp4 --id christmas_visuals --minx 0 --miny 0 --maxx 1920 --maxy 1080
python3 illuminate.py
rsync -Wravz -e "ssh -p 9000" --progress src "illuminate@comran.org:."
