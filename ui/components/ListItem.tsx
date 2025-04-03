import * as React from "react";
import { Movie } from "../interfaces";
import { PlusButton } from "./PlusButton";




export const ListItem = React.memo(({ 
  item, 
  index, 
  hoveredIndex, 
  setHoveredIndex, 
  onClick 
}: { 
  item: Movie; 
  index: number; 
  hoveredIndex: number | null; 
  setHoveredIndex: (index: number | null) => void; 
  onClick?: () => void; 
}) => {
  return (
    <li
      key={item.id}
      style={{
        backgroundColor: hoveredIndex === index ? "rgba(109, 152, 199, 0.69)" : "transparent",
        transition: "background-color 200ms ease",
        cursor: "pointer",
        padding: "10px 16px", 
      }}
      onMouseEnter={() => setHoveredIndex(index)}
      onMouseLeave={() => setHoveredIndex(null)}
    >
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(5, 1fr)",
        }}
      >
        <span style={{ fontSize: "16px" }}>{item.title}</span>
        <span style={{ fontSize: "16px" }}>{item.release_date}</span>
        <span style={{ fontSize: "16px" }}>{item.vote_average}</span>
        <span style={{ fontSize: "16px" }}>{item.vote_average}</span>
        <PlusButton index={index} hoveredIndex={hoveredIndex} onClick={onClick}/>
      </div>
    </li>
  );
});