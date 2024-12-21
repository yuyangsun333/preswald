const ButtonWidget = ({ label, onClick }) => {
  return (
    <button
      type="button"
      onClick={onClick || (() => alert("Button clicked!"))}
      className="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
    >
      {label}
    </button>
  );
};

export default ButtonWidget;
