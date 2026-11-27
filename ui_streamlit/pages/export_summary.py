import streamlit as st
import pandas as pd
from datetime import datetime
from db_management.database_manager import DatabaseManager

from helper_file.get_exporter import get_exporter

db_manager = DatabaseManager()

st.title("Export Facturen")

st.info("Deze pagina toont een overzicht van de te exporteren facturen.")

validated_invoices = db_manager.get_invoices_by_status("VALIDATED") 

if validated_invoices:
    df=pd.DataFrame(validated_invoices)
    
    st.metric("Aantal gevalideerde facturen", len(df))
    
    st.dataframe(df,use_container_width=True, hide_index=True)


    export_type=st.selectbox("Select export type", [
            "CSV",
            "Excel",
            "JSON",
            "PDF",
            "UBL XML",
            "Exact XML",
            "Twinfield XML"])
    
    EXPORT_MAP = {
                "CSV": "csv",
                "Excel": "excel",
                "JSON": "json",
                "PDF": "pdf",
                "UBL XML": "ubl",
                "Exact XML": "exact",
                "Twinfield XML": "twinfield"
            }
    
        
        
        
    try:
        exporter = get_exporter(EXPORT_MAP.get(export_type), df)
        data=exporter.export()  
        
        if export_type.lower() == "csv":
            st.download_button(
                label="Download CSV",
                data=data,
                file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        elif export_type.lower() == "excel":
            st.download_button(
                label="Download Excel",
                data=data,
                file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif export_type.lower() == "json":
            st.download_button(
                label="Download JSON",
                data=data,
                file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        elif export_type.lower() == "pdf":
            st.download_button(
                label="Download PDF",
                data=data,
                file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        elif export_type.lower() == "ubl xml":
            st.download_button(
                label="Download UBL XML",
                data=data,
                file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml",
                mime="application/xml"
            )
        elif export_type.lower() == "exact xml":
            st.download_button(
                label="Download Exact XML",
                data=data,
                file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml",
                mime="application/xml"
            )
        elif export_type.lower() == "twinfield xml":
            st.download_button(
                label="Download Twinfield XML",
                data=data,
                file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml",
                mime="application/xml"
            )   
        
        st.success(f"Facturen succesvol geëxporteerd als {export_type}")
        
    except ValueError as e:
        st.error(str(e))
    
    
    