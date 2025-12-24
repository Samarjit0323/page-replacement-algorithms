import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Page Replacement Simulator")

st.markdown("""
<style>
    .grid-container {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 10px;
        overflow-x: auto;
        padding: 20px 0;
    }
    .grid-column {
        display: flex;
        flex-direction: column;
        gap: 8px;
        min-width: 60px;
        align-items: center;
    }
    .cell {
        width: 55px;
        height: 55px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #d1d5db;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.2rem;
        background-color: #ffffff;
    }
    .header-cell { border: none; color: #6b7280; font-size: 0.8rem; height: 20px; }
    .input-cell { background-color: #3b82f6; color: white; border-color: #2563eb; }
    .fault-cell { background-color: #fee2e2; border-color: #ef4444; color: #b91c1c; }
    .hit-cell { background-color: #f3f4f6; color: #374151; }
    .status-cell { border: none; font-size: 1.5rem; height: 40px; }
    .label-column { font-weight: bold; color: #4b5563; text-align: right; padding-right: 10px; min-width: 80px; }
</style>
""", unsafe_allow_html=True)

def simulate_paging(ref_string, num_frames, algo):
    pages = [p.strip() for p in ref_string.split(',') if p.strip()]
    frames = [None] * num_frames
    history = []
    faults = 0
    fifo_queue = [] 

    for i, page in enumerate(pages):
        is_fault = False
        
        if page not in frames:
            is_fault = True
            faults += 1
            
            if None in frames:
                target_idx = frames.index(None)
                frames[target_idx] = page
                fifo_queue.append(target_idx)
            else:
                if algo == 'FIFO':
                    target_idx = fifo_queue.pop(0)
                    frames[target_idx] = page
                    fifo_queue.append(target_idx)
                
                elif algo == 'LRU':
                    past_refs = pages[:i]
                    last_seen = {f: len(past_refs) - 1 - past_refs[::-1].index(f) for f in frames}
                    victim_page = min(last_seen, key=last_seen.get)
                    target_idx = frames.index(victim_page)
                    frames[target_idx] = page
                
                elif algo == 'Optimal':
                    future_refs = pages[i+1:]
                    farthest_idx = -1
                    target_idx = 0
                    for idx, f in enumerate(frames):
                        if f not in future_refs:
                            target_idx = idx
                            break
                        else:
                            first_occurrence = future_refs.index(f)
                            if first_occurrence > farthest_idx:
                                farthest_idx = first_occurrence
                                target_idx = idx
                    frames[target_idx] = page
        
        history.append({
            "page": page,
            "frames": list(frames),
            "is_fault": is_fault,
            "replaced_idx": frames.index(page) if is_fault else -1
        })
    return faults, history

st.title("Virtual Memory Management: Page Replacement Simulator")
st.markdown("Visualize how the OS manages physical memory frames using different algorithms.")

with st.sidebar:
    st.header("Input Parameters")
    ref_input = st.text_input("Reference String (comma separated)")
    frame_count = st.number_input("Number of Frames",min_value=1, max_value=20,value=3,step=1) 
    run = st.button("▶ Run Simulation")
    if not run:
        st.info("Enter inputs and Run")
        st.stop()
    if not ref_input.strip():
        st.warning("Reference string cannot be empty.")
        st.stop()

algos = ["FIFO", "LRU", "Optimal"]
tabs = st.tabs(algos)
fifo="FIFO replaces the page that has been in memory for the longest time, regardless of how frequently or recently it is used."
lru="LRU replaces the page that has not been used for the longest period of time in the past."
opt="Optimal replaces the page that will not be used for the longest time in the future."
desc=[fifo,lru,opt]

for i, algo_name in enumerate(algos):
    with tabs[i]:
        st.info(desc[i])
        if [int(p.strip()) for p in ref_input.split(',') if p.strip()]==[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 ] and algo_name == "FIFO":
            st.error("This reference string shows Belady's Anomaly",icon=":material/info:")

        faults, steps = simulate_paging(ref_input, frame_count, algo_name)
        
        col1, col2 = st.columns(2)
        col1.metric("Total Page Faults", faults)
        col2.metric("Page Fault Rate", f"{round((faults/len(steps))*100, 1)}%")

        html_output = '<div class="grid-container">'
        html_output += '<div class="grid-column label-column">'
        html_output += '<div class="header-cell"></div>'
        html_output += '<div class="left-label" style="height:55px; display:flex; align-items:center; justify-content:flex-end;">Input</div>'
        for f in range(frame_count):
            html_output += f'<div class="left-label" style="height:55px; display:flex; align-items:center; justify-content:flex-end;">Slot {f}</div>'
        html_output += '<div class="left-label" style="height:40px; display:flex; align-items:center; justify-content:flex-end;">Status</div>'
        html_output += '</div>'

        for step_idx, s in enumerate(steps):
            html_output += '<div class="grid-column">'
            html_output += f'<div class="header-cell">Step {step_idx+1}</div>'

            html_output += f'<div class="cell input-cell">{s["page"]}</div>'

            for f_idx in range(frame_count):
                val = s['frames'][f_idx] if s['frames'][f_idx] is not None else "-"
                cls = "fault-cell" if s['is_fault'] and s['replaced_idx'] == f_idx else "hit-cell"
                html_output += f'<div class="cell {cls}">{val}</div>'

            icon = "❌" if s['is_fault'] else "✅"
            html_output += f'<div class="status-cell">{icon}</div>'
            html_output += '</div>'
            
        html_output += '</div>'
        st.markdown(html_output, unsafe_allow_html=True)

st.success("Simulation complete. Switch tabs to compare algorithms")
