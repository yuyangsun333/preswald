const SpinnerWidget = ({ label = "Loading..." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-4">
      {label && (
        <p className="mb-3 text-sm font-medium text-gray-900">{label}</p>
      )}
      <div className="w-6 h-6 border-4 border-gray-300 border-t-blue-600 rounded-full animate-spin"></div>
    </div>
  );
};

export default SpinnerWidget;
