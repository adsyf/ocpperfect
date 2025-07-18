# OCPPerfect
docker run -d --name rabbitmq --restart unless-stopped -p 5672:5672 -p 15672:15672 rabbitmq:4-management  
pip install -r requirements.txt  
python ocpp_server.py  
python queue_client.py queue_message_1  
python websocket_client_just_listening.py
## this is for manual testing  
python websocket_client
$env:PYTHONPATH="D:\OCPPerfect\ocpperfect\"


## testing docs
https://realpython.com/python-testing/#automated-vs-manual-testing
https://medium.com/@dndelucca/recommendation-algorithm-using-python-and-rabbitmq-part-2-connecting-with-rabbitmq-aa0ec933e195 (https://github.com/delucca-articles/rabbitmq-python-adapter?source=post_page-----aa0ec933e195---------------------------------------)
