import React, { useState } from "react";

interface MagazineCardProps {
  magazine: Magazine;
  onEdit: () => void;
  onManageArticles: () => void;
  onUploadArticle: () => void;
  toggleExpansion: () => void;
  expanded: boolean;
}

const MagazineCard: React.FC<MagazineCardProps> = ({
  magazine,
  onEdit,
  onManageArticles,
  onUploadArticle,
  toggleExpansion,
  expanded,
}) => {
  if (!magazine || !magazine.id) {
    return null;
  }

  return (
    <div className="col-4 mb-3" key={magazine.id}>
      <div className="card p-3">
        <h5>{magazine.name}</h5>
        <p>
          <strong>Publisher:</strong> {magazine.publisher}
        </p>
        <p>
          <strong>Edition:</strong> {magazine.edition}
        </p>
        <button
          className="btn btn-link p-0"
          onClick={() => toggleExpansion()}
        >
          {expanded ? "Hide Details" : "Show Details"}
        </button>
        {expanded && (
          <div className="mt-2">
            <p>
              <strong>Abstract:</strong> {magazine.abstract}
            </p>
            <p>
              <strong>Categories:</strong> {magazine.categories.join(", ")}
            </p>
            <p>
              <strong>Genres:</strong> {magazine.genres.join(", ")}
            </p>
            <p>
              <strong>Created On:</strong> {magazine.createdOn.toDateString()}
            </p>
            <p>
              <strong>Edited On:</strong> {magazine.editedOn.toDateString()}
            </p>
            <p>
              <strong>Date:</strong> {magazine.date.toDateString()}
            </p>
          </div>
        )}
        <button
          className="btn btn-primary mt-2"
          onClick={() => onUploadArticle()}
        >
          Upload Article
        </button>
        <button
          className="btn btn-secondary mt-2"
          onClick={() => onEdit()}
        >
          Edit Magazine
        </button>
        <button
          className="btn btn-warning mt-2"
          onClick={() => onManageArticles()}
        >
          Manage Articles
        </button>
      </div>
    </div>
  );
};

export default MagazineCard;
