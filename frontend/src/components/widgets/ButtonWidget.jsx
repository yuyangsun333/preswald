const ButtonWidget = ({ label }) => {
  return (
    <button onClick={() => alert("Button clicked!")}>
      {label}
    </button>
  );
};

export default ButtonWidget;
