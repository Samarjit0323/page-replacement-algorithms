import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="OS Memory Simulator")

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
        total_faults, steps = simulate_paging(ref_input, frame_count, algo_name)
        
        col1, col2 = st.columns(2)
        col1.metric("Total Page Faults", total_faults)
        col2.metric("Page Fault Rate", f"{round((total_faults/len(steps))*100, 1)}%")

        st.subheader(f"Vertical Frame Map: {algo_name}")

        ui_cols = st.columns([1.2] + [1] * len(steps))

        for idx, s in enumerate(steps):
            ui_cols[idx+1].button(s['page'], key=f"{algo_name}_ref_{idx}") 

        st.markdown("---")
        
        for f_idx in range(frame_count):
            for step_idx, s in enumerate(steps):
                val = s['frames'][f_idx] if s['frames'][f_idx] is not None else "-"
                if s['is_fault'] and s['replaced_idx'] == f_idx:
                    ui_cols[step_idx+1].error(f"**{val}**")
                else:
                    ui_cols[step_idx+1].code(val)

        for idx, s in enumerate(steps):
            if s['is_fault']:
                ui_cols[idx+1].markdown("❌")
            else:
                ui_cols[idx+1].markdown("✅")

st.success("Simulation complete. Switch tabs to compare algorithms")