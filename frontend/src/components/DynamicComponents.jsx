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
    console.log(`[DynamicComponents] Component update triggered:`, {
      componentId,
      value,
      timestamp: new Date().toISOString()
    });
    onComponentUpdate(componentId, value);
  };

  return (
    <div className="flex flex-wrap gap-4 p-4">
      {components.map((component, index) => {
        const componentId = component.id || `component-${index}`;
        let renderedComponent;

        switch (component.type) {
          case "button":
            renderedComponent = (
              <ButtonWidget
                key={componentId}
                {...component}
                onClick={() => {
                  console.log(`[Button] Clicked:`, componentId);
                  handleUpdate(componentId, true);
                }}
              />
            );
            break;
          case "slider":
            renderedComponent = (
              <SliderWidget
                key={componentId}
                {...component}
                value={component.value}
                onChange={(value) => {
                  console.log(`[Slider] Value changed:`, { componentId, value });
                  handleUpdate(componentId, value);
                }}
              />
            );
            break;
          case "text_input":
            renderedComponent = (
              <TextInputWidget
                key={componentId}
                {...component}
                value={component.value}
                onChange={(value) => {
                  console.log(`[TextInput] Value changed:`, { componentId, value });
                  handleUpdate(componentId, value);
                }}
              />
            );
            break;
          case "checkbox":
            renderedComponent = (
              <CheckboxWidget
                key={componentId}
                {...component}
                checked={component.value}
                onChange={(value) => {
                  console.log(`[Checkbox] Value changed:`, { componentId, value });
                  handleUpdate(componentId, value);
                }}
              />
            );
            break;
          case "selectbox":
            renderedComponent = (
              <SelectboxWidget
                key={componentId}
                {...component}
                value={component.value}
                onChange={(value) => {
                  console.log(`[Selectbox] Value changed:`, { componentId, value });
                  handleUpdate(componentId, value);
                }}
              />
            );
            break;
          case "progress":
            renderedComponent = (
              <ProgressWidget
                key={componentId}
                {...component}
                value={component.value}
              />
            );
            break;
          case "spinner":
            renderedComponent = (
              <SpinnerWidget
                key={componentId}
                {...component}
              />
            );
            break;
          case "alert":
            renderedComponent = (
              <AlertWidget
                key={componentId}
                {...component}
              />
            );
            break;
          case "image":
            renderedComponent = (
              <ImageWidget
                key={componentId}
                {...component}
              />
            );
            break;
          case "text":
            renderedComponent = (
              <MarkdownRendererWidget
                key={componentId}
                {...component}
              />
            );
            break;
          case "table":
            renderedComponent = (
              <TableViewerWidget 
                key={componentId} 
                data={component.data} 
              />
            );
            break;
          case "connection":
            renderedComponent = (
              <ConnectionInterfaceWidget 
                key={componentId} 
              />
            );
            break;
          case "plot":
            renderedComponent = (
              <DataVisualizationWidget 
                key={componentId} 
                data={component.data} 
              />
            );
            break;
          default:
            renderedComponent = (
              <UnknownWidget 
                key={componentId} 
              />
            );
            break;
        }

        return (
          <div
            key={componentId}
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
