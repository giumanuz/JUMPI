import React, { useState } from "react";

interface ArticleCardProps {
  article: {
    id: string;
    title: string;
    author: string;
    content: string;
    createdOn: Date;
  };
  onEdit: () => void;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article, onEdit }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded((prev) => !prev);
  };

  return (
    <div className="card mb-3 h-100 d-flex flex-column p-3">
      <div className="mb-3">
        <h5>{article.title}</h5>
        <small className="text-muted">
          Author: {article.author} | Created on:{" "}
          {article.createdOn.toLocaleDateString()}
        </small>
      </div>

      <div className="mb-3 flex-grow-1">
        <p className="card-text">
          {isExpanded
            ? article.content
            : `${article.content.substring(0, 400)}...`}
        </p>
        <button className="btn btn-link p-0" onClick={toggleExpand}>
          {isExpanded ? "Collapse" : "Read more"}
        </button>
      </div>

      <div className="mt-auto">
        <button className="btn btn-primary" onClick={onEdit}>
          Edit Article
        </button>
      </div>
    </div>
  );
};

export default ArticleCard;
