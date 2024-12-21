import React from "react";
import ButtonWidget from "./widgets/ButtonWidget";
import SliderWidget from "./widgets/SliderWidget";
import TextInputWidget from "./widgets/TextInputWidget";
import CheckboxWidget from "./widgets/CheckboxWidget";
import SelectboxWidget from "./widgets/SelectboxWidget";
import ProgressWidget from "./widgets/ProgressWidget";
import SpinnerWidget from "./widgets/SpinnerWidget";
import AlertWidget from "./widgets/AlertWidget";
import ImageWidget from "./widgets/ImageWidget";
import MarkdownRendererWidget from "./widgets/MarkdownRendererWidget";
import TableViewerWidget from "./widgets/TableViewerWidget";
import ConnectionInterfaceWidget from "./widgets/ConnectionInterfaceWidget";
import UnknownWidget from "./widgets/UnknownWidget";
import DataVisualizationWidget from "./widgets/DataVisualizationWidget";

const DynamicWidgets = ({ components }) => {
  return (
    <div className="flex flex-wrap gap-4 p-4">
      {components.map((component, index) => {
        let renderedComponent;

        switch (component.type) {
          case "button":
            renderedComponent = <ButtonWidget key={index} label={component.label} />;
            break;
          case "slider":
            renderedComponent = (
              <SliderWidget
                key={index}
                label={component.label}
                min={component.min}
                max={component.max}
              />
            );
            break;
          case "text_input":
            renderedComponent = (
              <TextInputWidget
                key={index}
                label={component.label}
                placeholder={component.placeholder}
              />
            );
            break;
          case "checkbox":
            renderedComponent = (
              <CheckboxWidget
                key={index}
                label={component.label}
                defaultChecked={component.default}
              />
            );
            break;
          case "selectbox":
            renderedComponent = (
              <SelectboxWidget
                key={index}
                label={component.label}
                options={component.options}
                defaultOption={component.default}
              />
            );
            break;
          case "progress":
            renderedComponent = (
              <ProgressWidget
                key={index}
                label={component.label}
                value={component.value}
              />
            );
            break;
          case "spinner":
            renderedComponent = <SpinnerWidget key={index} label={component.label} />;
            break;
          case "alert":
            renderedComponent = (
              <AlertWidget
                key={index}
                message={component.message}
                level={component.level}
              />
            );
            break;
          case "image":
            renderedComponent = (
              <ImageWidget key={index} src={component.src} alt={component.alt} />
            );
            break;
          case "text":
            renderedComponent = (
              <MarkdownRendererWidget
                key={index}
                markdown={component.content}
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

export default DynamicWidgets;
