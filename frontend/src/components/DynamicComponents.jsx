import AlertWidget from "./widgets/AlertWidget";
import ButtonWidget from "./widgets/ButtonWidget";
import CheckboxWidget from "./widgets/CheckboxWidget";
import ConnectionInterfaceWidget from "./widgets/ConnectionInterfaceWidget";
import DataVisualizationWidget from "./widgets/DataVisualizationWidget";
import ImageWidget from "./widgets/ImageWidget";
import MarkdownRendererWidget from "./widgets/MarkdownRendererWidget";
import ProgressWidget from "./widgets/ProgressWidget";
import React from "react";
import SelectboxWidget from "./widgets/SelectboxWidget";
import SliderWidget from "./widgets/SliderWidget";
import SpinnerWidget from "./widgets/SpinnerWidget";
import TableViewerWidget from "./widgets/TableViewerWidget";
import TextInputWidget from "./widgets/TextInputWidget";
import UnknownWidget from "./widgets/UnknownWidget";

const DynamicComponents = ({ components, onComponentUpdate }) => {
  const handleUpdate = (componentId, value) => {
    onComponentUpdate(componentId, value);
  };

  return (
    <div className="flex flex-wrap gap-4 p-4">
      {components.map((component, index) => {
        let renderedComponent;

        switch (component.type) {
          case "button":
            renderedComponent = (
              <ButtonWidget
                key={component.id}
                {...component}
                onClick={() => handleUpdate(component.id, true)}
              />
            );
            break;
          case "slider":
            renderedComponent = (
              <SliderWidget
                key={component.id}
                {...component}
                onChange={(value) => handleUpdate(component.id, value)}
              />
            );
            break;
          case "text_input":
            renderedComponent = (
              <TextInputWidget
                key={component.id}
                {...component}
                onChange={(value) => handleUpdate(component.id, value)}
              />
            );
            break;
          case "checkbox":
            renderedComponent = (
              <CheckboxWidget
                key={component.id}
                {...component}
                onChange={(value) => handleUpdate(component.id, value)}
              />
            );
            break;
          case "selectbox":
            renderedComponent = (
              <SelectboxWidget
                key={component.id}
                {...component}
                onChange={(value) => handleUpdate(component.id, value)}
              />
            );
            break;
          case "progress":
            renderedComponent = (
              <ProgressWidget
                key={component.id}
                {...component}
              />
            );
            break;
          case "spinner":
            renderedComponent = (
              <SpinnerWidget
                key={component.id}
                {...component}
              />
            );
            break;
          case "alert":
            renderedComponent = (
              <AlertWidget
                key={component.id}
                {...component}
              />
            );
            break;
          case "image":
            renderedComponent = (
              <ImageWidget
                key={component.id}
                {...component}
              />
            );
            break;
          case "text":
            renderedComponent = (
              <MarkdownRendererWidget
                key={component.id}
                {...component}
              />
            );
            break;
          case "table":
            renderedComponent = <TableViewerWidget key={index} data={component.data} />;
            break;
          case "connection":
            renderedComponent = <ConnectionInterfaceWidget key={index} />;
            break;
          case "plot":
            renderedComponent = <DataVisualizationWidget key={index} data={component.data} />;
            break;
          default:
            renderedComponent = <UnknownWidget key={index} />;
            break;
        }

        return (
          <div
            key={index}
            className="flex-1 min-w-[250px] max-w-[33%] p-4 bg-white border border-gray-200 rounded-md shadow-sm"
          >
            {renderedComponent}
          </div>
        );
      })}
    </div>
  );
};

export default DynamicComponents;
