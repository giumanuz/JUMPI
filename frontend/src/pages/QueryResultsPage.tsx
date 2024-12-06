import React from "react";
import { useLocation } from "react-router-dom";
import MagazineCard from "../components/MagazineCard";

const QueryResultPage = () => {
  const location = useLocation();
  const results = location.state?.results?.hits?.hits ?? [];

  return (
    <div className="container mt-4">
      <h1>Search Results</h1>
      {results.length === 0 ? (
        <p>No results found.</p>
      ) : (
        results.map((result: any) => (
          <MagazineCard
            key={result._id}
            data={{
              ...result._source,
              _id: result._id,
            }}
          />
        ))
      )}
    </div>
  );
};

export default QueryResultPage;
