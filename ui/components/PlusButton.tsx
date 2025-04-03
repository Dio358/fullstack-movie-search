import * as React from "react";
import ControlPointIcon from '@mui/icons-material/ControlPoint';
import { Movie } from "../interfaces";


export const PlusButton = React.memo(({ index, hoveredIndex, onClick } : {index: number, hoveredIndex: number | null, onClick?: () => void; }) => {
  const [isFocusedHover, setIsFocusedHover] = React.useState(false);

  const getColor = (): string => {
    if (isFocusedHover) return "rgba(0, 0, 0, 1)";
    if (index === hoveredIndex) return "rgba(0, 0, 0, 0.68)";
    return "rgba(0, 0, 0, 0.34)";
  };

  return (
    <ControlPointIcon
      style={{
        color: getColor(),
        transition: "color 150ms ease",
        cursor: "pointer",
      }}
      onMouseEnter={() => setIsFocusedHover(true)}
      onMouseLeave={() => setIsFocusedHover(false)}
      onClick={onClick}
    />
  );
}, (prevProps, nextProps) => (
  // Only re-render if this button's hover state changes
  prevProps.index === nextProps.index &&
  prevProps.hoveredIndex === nextProps.hoveredIndex
));