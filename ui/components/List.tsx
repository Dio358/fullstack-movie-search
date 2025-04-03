import * as React from "react";
import { Movie } from "../interfaces";
import { useEffect } from "react";
import styles from './scrollableList.module.css';
import {ListItem} from './ListItem'

type Props = {
  items: Movie[];
  maxHeight?: string;
  length?: number
  onClick?: (movie: Movie) => void;
  onHover?: (index: Movie | null) => void | null;
  action: string;
};


const List: React.FC<Props> = ({ items, maxHeight = "300px", length = Number.POSITIVE_INFINITY, onClick, onHover = null, action }) => {
  const [hoveredIndex, setHoveredIndex] = React.useState<number | null>(null);
  const [highlightPlus, setHighlightPlus] = React.useState<boolean>(false);
  
  useEffect(() => {
    if (onHover) {
      onHover(items?.at(hoveredIndex) || null);
    }
  }, [hoveredIndex, onHover, items]);

  // Memoize the list items to prevent re-rendering when hoveredIndex changes
  const memoizedListItems = React.useMemo(() => {
    if (!Array.isArray(items)) return null;
    return items && items.slice(0, length).map((item, index) => (
      <ListItem
        key={item.id}
        item={item}
        index={index}
        hoveredIndex={hoveredIndex}
        setHoveredIndex={setHoveredIndex}
        onClick={() => onClick(item)}
      />
    ));
  }, [items, length, hoveredIndex, onClick]);

  return (
    <>
      <span>Click row to {action} favorites</span>
      <div style={{
        width: "95%",
        borderRadius: "5px",
        overflow: "hidden",
      }}>
        {/* Header */}
        <div style={{
          backgroundColor: "rgba(17, 124, 231, 0.63)",
          display: "grid",
          gridTemplateColumns: "repeat(5, 1fr)",
          padding: "16px",
          borderTopLeftRadius: "5px",
          borderTopRightRadius: "5px",
        }}>
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
          <ul style={{ 
            listStyleType: "none", 
            padding: 0, 
            margin: 0 
          }}>
            {memoizedListItems}
          </ul>
        </div>
      </div>
    </>
  );
};

export default List;