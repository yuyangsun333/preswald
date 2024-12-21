document.addEventListener("DOMContentLoaded", () => {
  console.log("JavaScript is working!");
  const button = document.getElementById("exampleButton");
  if (button) {
    button.addEventListener("click", () => {
      alert("Button clicked!");
    });
  }
});
