from preswald import text, checkbox, slider, button, selectbox, text_input, progress, spinner, alert, image

text("# Welcome to Preswald!")
text("This is your first app. 🎉")

checkbox("Check me")

slider("Adjust value", 0, 100, 25)

button("Click me")

selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])

text_input("Enter your name")

progress("Loading progress", 0.5)

spinner("Loading...")

alert("This is an alert")

image("https://picsum.photos/200/300")
