import { Movie } from "../interfaces";
import { useEffect, useState, useMemo } from "react";
import styles from "./scrollableList.module.css";
import { ListItem } from "./ListItem";

type Props = {
  items: Movie[] | null;
  maxHeight?: string;
  length?: number;
  onHover?: (index: Movie | null) => void | null;
  action: string;
};

const List: React.FC<Props> = ({
  items,
  maxHeight = "300px",
  length = Number.POSITIVE_INFINITY,
  onHover = null,
}) => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  useEffect(() => {
    if (onHover) {
      onHover(
        hoveredIndex
          ? items?.[hoveredIndex]
            ? items?.[hoveredIndex]
            : null
          : null
      );
    }
  }, [hoveredIndex, onHover, items]);

  // Memoize the list items to prevent re-rendering when hoveredIndex changes
  const memoizedListItems = useMemo(() => {
    if (!Array.isArray(items)) return null;
    return (
      items &&
      items
        .slice(0, length)
        .map((item, index) => (
          <ListItem
            key={item.id}
            item={item}
            index={index}
            hoveredIndex={hoveredIndex}
            setHoveredIndex={setHoveredIndex}
          />
        ))
    );
  }, [items, length, hoveredIndex]);

  return (
    <>
      <div
        style={{
          width: "95%",
          borderRadius: "5px",
          overflow: "hidden",
        }}
      >
        {/* Header */}
        <div
          style={{
            backgroundColor: "rgba(17, 124, 231, 0.63)",
            display: "grid",
            gridTemplateColumns: "repeat(5, 1fr)",
            padding: "16px",
            borderTopLeftRadius: "5px",
            borderTopRightRadius: "5px",
          }}
        >
          <span style={{ fontSize: "16px" }}>Title</span>
          <span style={{ fontSize: "16px" }}>Release Date</span>
          <span style={{ fontSize: "16px" }}>Rating</span>
          <span style={{ fontSize: "16px" }}>Genres</span>
          <span style={{ fontSize: "16px" }}>+</span>
        </div>

        {/* Content */}
        <div
          className={styles.scrollable}
          style={{
            background: "white",
            borderBottomLeftRadius: "5px",
            borderBottomRightRadius: "5px",
            maxHeight: maxHeight,
            overflowY: "auto",
          }}
        >
          <ul
            style={{
              listStyleType: "none",
              padding: 0,
              margin: 0,
            }}
          >
            {memoizedListItems}
          </ul>
        </div>
      </div>
    </>
  );
};

export default List;
