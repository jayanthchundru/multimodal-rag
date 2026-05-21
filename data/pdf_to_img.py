import os 
from pathlib import Path 
from pdf2image import convert_from_path
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s -- %(levelname)s -- %(message)s"
)

logger = logging.getLogger(__name__)

def setup_output_folder(output_folder):
    '''
    Set the output folder dir, or creates new if the dir doesn't exists
    '''
    
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    logger.info(f"Output folder : {output_folder}")

def get_pdf_files(pdf_folder):
    '''
    Get all the files from the pdf folder
    '''
    
    pdf_folder = Path(pdf_folder)
    if not pdf_folder.exists():
        raise FileNotFoundError(f"PDF folder not found: {pdf_folder}")
    
    pdf_files = list(pdf_folder.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError (f"No .pdf files found in the {pdf_folder}")
    
    logger.info(f"Found {len(pdf_files)} PDF files")
    
    return pdf_files

def sanitize_filename(filename):
    '''
    Removes the .pdf extension and replace spaces with underscores.
    '''
    
    return Path(filename).stem.replace(".pdf", "_").lower()

def convert_pdf_to_images(pdf_path, output_subfolder, dpi):
    try:
        logger.info(f"Converting {pdf_path.name} at {dpi} DPI ")
        
        Path(output_subfolder).mkdir(parents=True, exist_ok=True)
        
        pages = convert_from_path(str(pdf_path), dpi=dpi)
        
        logger.info(f"Rendered {len(pages)} pages from {pdf_path.name}")
        
        for page_num, page_image in enumerate(pages, start=1):
            output_path = Path(output_subfolder)/f"page_{page_num:03d}.png"
            page_image.save(str(output_path), "PNG")
            
        logger.info(f" Saved {len(pages)} pages to {output_subfolder}")
        
        return True, len(pages), None
    
    except Exception as e:
        error_msg = f"Error converting {pdf_path.name}: {str(e)}"
        logger.error(error_msg)
        return False, 0, error_msg



def main():
    parser = argparse.ArgumentParser(description="Convert PDFs to Images with the specified DPI")
    parser.add_argument("--pdf-folder", type=str, required=True, help="Enter the Pdfs folder to convert into images")
    parser.add_argument("--output-folder", type=str, required=True, help="Desired output path to save the converted images")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for rendering ( default = 150)")
    
    args = parser.parse_args()
    
    logger.info("="*60)
    logger.info("Converting Pdf to Images")
    logger.info("="*60)
    logger.info(f"Pdf folder: {args.pdf_folder}, Output folder: {args.output_folder}, DPI : {args.dpi}")
    logger.info("="*60)
    
    try: 
        setup_output_folder(args.output_folder)
        pdf_files = get_pdf_files(args.pdf_folder)
        
        results = []
        for idx, pdf_path in enumerate(pdf_files, start=1):
            logger.info(f"\n[{idx}/ {len(pdf_files)} Processing {pdf_path.name}]")
            subfolder_name = sanitize_filename(pdf_path.name)
            output_subfolder = Path(args.output_folder) / subfolder_name
            
            success, page_count, error_msg = convert_pdf_to_images(pdf_path, output_subfolder, dpi=args.dpi)
            
            results.append({
                'pdf' : pdf_path.name,
                'success': success,
                'page_count' : page_count, 
                'error': error_msg
            })
            
        logger.info("\n" + "=" * 60)
        logger.info("Conversion Summary")
        logger.info("="*60)
        
        successful = sum(1 for r in results if r['success'])
        failed = sum(1 for r in results if not r['success'])
        total_pages = sum(r['page_count'] for r in results)
        
        logger.info(f"successful : {successful} failed : {failed} total_pages : {total_pages}")
        
    except Exception as e:
        logger.error(f"Fatal error : {str(e)}")
        raise
    
if __name__ == "__main__":
    main()