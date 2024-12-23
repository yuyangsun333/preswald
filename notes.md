1/ when we declare some components in hello.py, they needs to be passed to the frontend and we need to render the frontend in the browser
2/ preswald server will be serving on some port, but / route will be serving the frontend app's index.html file, and /api/\* will be serving from the @preswald server
3/ we need to make sure that the components that are present in the hello.py are passed to the frontend and rendered in the browser via websockets
4/ the initialisation should be done properly, first getting the components declared in the hello.py file and then passing them to the frontend
5/ the websocket connection should be established properly, and the components should be rendered in the browser via websockets
6/ the components should be rendered in the browser via websockets, and the websocket connection should be established properly