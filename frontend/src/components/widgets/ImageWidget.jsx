const ImageWidget = ({ src, alt, size = "medium", rounded = true }) => {
  // Define size classes based on the provided size prop
  const sizeClasses = {
    small: "w-24 h-24",
    medium: "w-48 h-48",
    large: "w-96 h-96",
    full: "w-full h-auto",
  };

  return (
    <div>
      <img
        src={src}
        alt={alt}
        className={`object-cover ${sizeClasses[size]} transition-transform duration-200 hover:scale-105`}
      />
    </div>
  );
};

export default ImageWidget;
