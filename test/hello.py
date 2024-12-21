from preswald import text, slider, checkbox, button, selectbox, text_input, progress, spinner, alert, image

text("# Welcome to Preswald!")
text("## This is your first app. 🎉")
slider("Slider", min_val=0, max_val=100)
checkbox("Check me")
button("Click me")
selectbox("Select me", options=["Option 1", "Option 2", "Option 3"])
text_input(label="Type here", placeholder="Type something here")
progress(label="Progress", value=50)
spinner(label="Loading...")
alert(message="This is an alert!", level="info")
image(src="https://cdn.pixabay.com/photo/2020/07/21/01/33/cute-5424776_1280.jpg",
      alt="Placeholder image")
