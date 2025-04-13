import { memo } from "react";
import { Movie } from "../../interfaces";
import { AddToFavoritesButton } from "../buttons/AddToFavoritesButton";

export const ListItem = memo(
  ({
    item,
    index,
    hoveredIndex,
    setHoveredIndex,
  }: {
    item: Movie;
    index: number;
    hoveredIndex: number | null;
    setHoveredIndex: (index: number | null) => void;
  }) => {
    return (
      <li
        key={item.id}
        style={{
          backgroundColor:
            hoveredIndex === index
              ? "rgba(109, 152, 199, 0.69)"
              : "transparent",
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
          <span style={{ fontSize: "16px" }}>
            {item?.genres?.map((g) => g.name).join(", ") ?? item.vote_count}
          </span>
          <AddToFavoritesButton
            index={index}
            hoveredIndex={hoveredIndex}
            movie={item}
          />
        </div>
      </li>
    );
  }
);
