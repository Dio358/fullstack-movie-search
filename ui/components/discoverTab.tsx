import {useState} from "react";
import List from "./List";

export const DiscoverTab = (props: {
    items: ({ id: number; title: string; rating: string; release_date: string }) []
}) => {
    const [selectedLength, setSelectedLength] = useState(1);

    return <div style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginLeft: "20px",
        paddingLeft: "10%"
    }}>
        <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Popular Movies</h1>
        <select value={selectedLength} onChange={(e) => setSelectedLength(Number(e.target.value))}>
            {Array.from({length: 20}, (_, i) => (
                <option key={i + 1} value={i + 1}>
                    {i + 1}
                </option>
            ))}
        </select>
        <List items={props.items} action="add to"/>

        <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Movies in the Same
            Genres</h1>
        <List items={props.items} action="remove from"/>

        <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Movies with Similar
            Runtimes</h1>
        <List items={props.items} action="remove from"/>
    </div>;
}