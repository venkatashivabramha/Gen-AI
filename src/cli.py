"""
Command-Line Interface for Business Plan Generator
Alternative to GUI for automation and scripting
"""
import sys
import os
from pathlib import Path
import argparse
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.business_plan_generator import BusinessPlanGenerator
from config.config import BUSINESS_TYPES

def main():
    """Main CLI entry point"""
    
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description='Generate comprehensive business plans from the command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from description
  python src/cli.py --mode ai --description "Tech startup for AI-powered tools"
  
  # Generate from form data
  python src/cli.py --mode form --name "My Business" --industry "Technology"
  
  # Generate from template
  python src/cli.py --mode template --template "Technology Startup" --name "TechCorp"
  
  # Specify output formats
  python src/cli.py --mode ai --description "E-commerce store" --formats pdf html docx
        """
    )
    
    # Mode selection
    parser.add_argument(
        '--mode',
        choices=['form', 'ai', 'template'],
        required=True,
        help='Input mode: form (structured data), ai (natural language), or template'
    )
    
    # Common arguments
    parser.add_argument(
        '--name',
        help='Business name (required for form and template modes)'
    )
    
    parser.add_argument(
        '--formats',
        nargs='+',
        choices=['pdf', 'html', 'docx'],
        default=['pdf'],
        help='Output formats (default: pdf)'
    )
    
    parser.add_argument(
        '--provider',
        choices=['openai', 'anthropic'],
        default='openai',
        help='LLM provider (default: openai)'
    )
    
    # AI mode arguments
    parser.add_argument(
        '--description',
        help='Business description for AI mode'
    )
    
    # Template mode arguments
    parser.add_argument(
        '--template',
        choices=BUSINESS_TYPES,
        help='Business type template'
    )
    
    # Form mode arguments
    parser.add_argument('--industry', help='Industry/sector')
    parser.add_argument('--business-type', help='Type of business')
    parser.add_argument('--location', help='Business location')
    parser.add_argument('--target-market', help='Target market description')
    parser.add_argument('--products', help='Products/services offered')
    parser.add_argument('--revenue-model', help='Revenue model')
    parser.add_argument('--investment', help='Initial investment amount')
    parser.add_argument('--innovation', help='Innovation focus')
    parser.add_argument('--detailed-description', help='Detailed business description')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.mode == 'ai' and not args.description:
        parser.error("--description is required for AI mode")
    
    if args.mode == 'template' and not args.template:
        parser.error("--template is required for template mode")
    
    if args.mode in ['form', 'template'] and not args.name:
        parser.error("--name is required for form and template modes")
    
    # Initialize generator
    print("=" * 70)
    print("  Business Plan Generator - CLI")
    print("=" * 70)
    print(f"\nMode: {args.mode}")
    print(f"Provider: {args.provider}")
    print(f"Output formats: {', '.join(args.formats)}")
    print()
    
    try:
        generator = BusinessPlanGenerator(args.provider)
        
        # Generate based on mode
        if args.mode == 'form':
            result = generate_from_form(generator, args)
        elif args.mode == 'ai':
            result = generate_from_ai(generator, args)
        elif args.mode == 'template':
            result = generate_from_template(generator, args)
        
        # Display results
        print("\n" + "=" * 70)
        print("✅ Generation Complete!")
        print("=" * 70)
        
        if result['status'] == 'success':
            print("\nGenerated files:")
            for fmt, path in result['files'].items():
                print(f"  • {fmt.upper()}: {path}")
            
            print("\nSections generated:")
            for section in result['sections'].keys():
                print(f"  • {section}")
        else:
            print("\n❌ Generation failed")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def generate_from_form(generator, args):
    """Generate from form data"""
    
    business_data = {
        'business_name': args.name,
        'industry': args.industry or 'General',
        'business_type': args.business_type or 'Other',
        'location': args.location or 'United States',
        'target_market': args.target_market or 'To be determined',
        'products_services': args.products or 'To be determined',
        'revenue_model': args.revenue_model or 'To be determined',
        'initial_investment': args.investment or 'To be determined',
        'innovation_focus': args.innovation or 'To be determined',
        'description': args.detailed_description or f'A business in the {args.industry or "general"} industry.'
    }
    
    print("Generating from form data...")
    print(f"Business: {business_data['business_name']}")
    print(f"Industry: {business_data['industry']}")
    
    return generator.generate_from_form(business_data, args.formats)

def generate_from_ai(generator, args):
    """Generate from AI description"""
    
    print("Generating from AI description...")
    print(f"Description length: {len(args.description)} characters")
    
    return generator.generate_from_natural_language(args.description, args.formats)

def generate_from_template(generator, args):
    """Generate from template"""
    
    basic_info = {
        'business_name': args.name,
        'location': args.location or 'United States',
        'specific_focus': args.innovation or 'General focus'
    }
    
    print(f"Generating from template: {args.template}")
    print(f"Business: {args.name}")
    
    return generator.generate_from_template(args.template, basic_info, args.formats)

def interactive_mode():
    """Interactive CLI mode"""
    
    print("=" * 70)
    print("  Business Plan Generator - Interactive Mode")
    print("=" * 70)
    print()
    
    # Choose mode
    print("Select input mode:")
    print("1. Form-based input")
    print("2. AI description")
    print("3. Template-based")
    
    mode_choice = input("\nEnter choice (1-3): ").strip()
    
    if mode_choice == '1':
        return interactive_form_mode()
    elif mode_choice == '2':
        return interactive_ai_mode()
    elif mode_choice == '3':
        return interactive_template_mode()
    else:
        print("Invalid choice")
        sys.exit(1)

def interactive_form_mode():
    """Interactive form mode"""
    
    print("\n--- Form Input Mode ---\n")
    
    business_data = {}
    business_data['business_name'] = input("Business Name: ").strip()
    business_data['industry'] = input("Industry: ").strip()
    business_data['business_type'] = input("Business Type: ").strip()
    business_data['location'] = input("Location: ").strip()
    
    print("\nProvide a detailed description (end with empty line):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    business_data['description'] = '\n'.join(lines)
    
    business_data['target_market'] = input("\nTarget Market: ").strip()
    business_data['products_services'] = input("Products/Services: ").strip()
    business_data['revenue_model'] = input("Revenue Model: ").strip()
    business_data['initial_investment'] = input("Initial Investment: ").strip()
    business_data['innovation_focus'] = input("Innovation Focus: ").strip()
    
    # Output formats
    print("\nSelect output formats (space-separated, e.g., 'pdf html'):")
    print("Options: pdf html docx")
    formats_input = input("Formats: ").strip().lower()
    formats = formats_input.split() if formats_input else ['pdf']
    
    # Provider
    provider = input("\nLLM Provider (openai/anthropic) [openai]: ").strip() or 'openai'
    
    # Generate
    print("\n🚀 Generating business plan...\n")
    generator = BusinessPlanGenerator(provider)
    result = generator.generate_from_form(business_data, formats)
    
    return result

def interactive_ai_mode():
    """Interactive AI mode"""
    
    print("\n--- AI Description Mode ---\n")
    print("Describe your business idea (end with a line containing only 'END'):\n")
    
    lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)
    
    description = '\n'.join(lines)
    
    # Output formats
    print("\nSelect output formats (space-separated, e.g., 'pdf html'):")
    formats_input = input("Formats: ").strip().lower()
    formats = formats_input.split() if formats_input else ['pdf']
    
    # Provider
    provider = input("\nLLM Provider (openai/anthropic) [openai]: ").strip() or 'openai'
    
    # Generate
    print("\n🚀 Generating business plan...\n")
    generator = BusinessPlanGenerator(provider)
    result = generator.generate_from_natural_language(description, formats)
    
    return result

def interactive_template_mode():
    """Interactive template mode"""
    
    print("\n--- Template Mode ---\n")
    
    print("Available templates:")
    for i, template in enumerate(BUSINESS_TYPES, 1):
        print(f"{i}. {template}")
    
    choice = int(input("\nSelect template (1-{}): ".format(len(BUSINESS_TYPES)))) - 1
    template = BUSINESS_TYPES[choice]
    
    print(f"\nSelected: {template}\n")
    
    basic_info = {}
    basic_info['business_name'] = input("Business Name: ").strip()
    basic_info['location'] = input("Location: ").strip()
    basic_info['specific_focus'] = input("Specific Focus: ").strip()
    
    # Output formats
    print("\nSelect output formats (space-separated, e.g., 'pdf html'):")
    formats_input = input("Formats: ").strip().lower()
    formats = formats_input.split() if formats_input else ['pdf']
    
    # Provider
    provider = input("\nLLM Provider (openai/anthropic) [openai]: ").strip() or 'openai'
    
    # Generate
    print("\n🚀 Generating business plan...\n")
    generator = BusinessPlanGenerator(provider)
    result = generator.generate_from_template(template, basic_info, formats)
    
    return result

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # No arguments, run interactive mode
        interactive_mode()
    else:
        # Arguments provided, run normal CLI
        main()
