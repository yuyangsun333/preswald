const ProgressWidget = ({ label, value, steps }) => {
  const progressWidth = `${value}%`;

  return (
    <div>
      <h4 className="sr-only">Progress</h4>
      <p className="text-sm font-medium text-gray-900">{label}</p>
      <div aria-hidden="true" className="mt-4">
        {/* Progress bar */}
        <div className="overflow-hidden rounded-full bg-gray-200">
          <div
            style={{ width: progressWidth }}
            className="h-2 rounded-full bg-blue-600 transition-all duration-300"
          />
        </div>

        {/* Steps */}
        {steps && (
          <div className="mt-4 grid grid-cols-4 text-sm font-medium text-gray-600">
            {steps.map((step, index) => (
              <div
                key={index}
                className={`text-center ${
                  index < steps.length * (value / 100)
                    ? "text-blue-600"
                    : "text-gray-600"
                }`}
              >
                {step}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProgressWidget;
