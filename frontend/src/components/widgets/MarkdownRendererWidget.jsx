import ReactMarkdown from "react-markdown";

const MarkdownRendererWidget = ({ markdown }) => {
  return (
    <div>
      <h3>Markdown Renderer</h3>
      <ReactMarkdown>{markdown}</ReactMarkdown>
    </div>
  );
};

export default MarkdownRendererWidget;
