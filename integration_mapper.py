"""
DeepSeek Extension - Integration Mapper
=====================================

Tạo sơ đồ liên kết tổng quan cho dự án deepseek-extension.
Phân tích dependencies, imports, exports và các mối quan hệ giữa các file.

Author: DeepSeek Extension Team
Date: September 2025
"""
import ast
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any
import Exception
import alias
import any
import cmd
import command
import config_file
import count
import d
import dep
import description
import dict
import dirs
import e
import enumerate
import exclude
import f
import file
import file_path
import files
import filter
import i
import imp
import integration
import isinstance
import issue
import len
import line
import list
import match
import next
import node
import open
import output_file
import path
import pkg
import print
import project_root
import rec
import req
import script
import self
import sorted
import step
import str
import ts_file
import version


class IntegrationMapper:

    def __init__(self: Any, project_root: str) -> Any:
        self.project_root = Path(project_root)
        self.integration_map = {'project_info': {}, 'core_files': {}, 'dependencies': {}, 'imports_exports': {}, 'integration_points': {}, 'build_flow': {}, 'runtime_flow': {}, 'issues': [], 'recommendations': []}
        self.exclude_dirs = {'node_modules', '.git', '.vscode', '__pycache__', 'out', 'dist', 'build', '.nyc_output', 'coverage', '.pytest_cache', 'venv', '.venv'}
        self.file_extensions = {'.ts', '.js', '.json', '.py', '.md', '.bat', '.ps1', '.yml', '.yaml', '.txt', '.sh'}

    def analyze_project(self: Any) -> dict[str, Any]:
        """Phân tích toàn bộ dự án và tạo integration map"""
        print('🔍 Bắt đầu phân tích integration...')
        self._collect_project_info()
        self._analyze_core_files()
        self._analyze_dependencies()
        self._analyze_imports_exports()
        self._find_integration_points()
        self._analyze_build_flow()
        self._analyze_runtime_flow()
        self._detect_issues_and_recommendations()
        print('✅ Hoàn thành phân tích!')
        return self.integration_map

    def _collect_project_info(self: Any) -> Any:
        """Thu thập thông tin cơ bản về dự án"""
        print('  📊 Thu thập thông tin dự án...')
        total_files = 0
        total_dirs = 0
        file_types = {}
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            total_dirs += len(dirs)
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    total_files += 1
                    ext = Path(file).suffix
                    file_types[ext] = file_types.get(ext, 0) + 1
        package_json_path = self.project_root / 'package.json'
        package_info = {}
        if package_json_path.exists():
            try:
                with open(package_json_path, encoding='utf-8') as f:
                    package_info = json.load(f)
            except:
                pass
        self.integration_map['project_info'] = {'name': package_info.get('name', 'Unknown'), 'version': package_info.get('version', 'Unknown'), 'description': package_info.get('description', ''), 'total_files': total_files, 'total_directories': total_dirs, 'file_types': file_types, 'analyzed_at': datetime.now().isoformat(), 'project_root': str(self.project_root)}

    def _analyze_core_files(self: Any) -> Any:
        """Phân tích các file core của extension"""
        print('  🎯 Phân tích core files...')
        core_files = {'package.json': 'Extension manifest & configuration', 'src/extension.ts': 'Main extension entry point', 'src/aiAgent.ts': 'AI Agent implementation', 'src/ai/ollamaClient.ts': 'Ollama API client', 'assistant.py': 'Python AI Assistant', 'tsconfig.json': 'TypeScript configuration', 'test-live.bat': 'Windows launcher script', 'run-deepseek.ps1': 'PowerShell orchestration', '.env': 'Environment variables', 'requirements.txt': 'Python dependencies'}
        for file_path, description in core_files.items():
            full_path = self.project_root / file_path
            file_info = {'description': description, 'exists': full_path.exists(), 'size': full_path.stat().st_size if full_path.exists() else 0, 'modified': datetime.fromtimestamp(full_path.stat().st_mtime).isoformat() if full_path.exists() else None}
            if full_path.exists():
                file_info.update(self._analyze_file_content(full_path))
            self.integration_map['core_files'][file_path] = file_info

    def _analyze_file_content(self: Any, file_path: Path) -> dict[str, Any]:
        """Phân tích nội dung của một file"""
        content_info = {'lines': 0, 'functions': [], 'classes': [], 'imports': [], 'exports': [], 'commands': [], 'errors': []}
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
                content_info['lines'] = len(content.splitlines())
                if file_path.suffix == '.ts':
                    content_info.update(self._analyze_typescript_file(content))
                elif file_path.suffix == '.py':
                    content_info.update(self._analyze_python_file(content))
                elif file_path.suffix == '.json':
                    content_info.update(self._analyze_json_file(content))
                elif file_path.suffix in ['.bat', '.ps1']:
                    content_info.update(self._analyze_script_file(content))
        except Exception as e:
            content_info['errors'].append(str(e))
        return content_info

    def _analyze_typescript_file(self: Any, content: str) -> dict[str, Any]:
        """Phân tích file TypeScript"""
        info = {'functions': [], 'classes': [], 'imports': [], 'exports': [], 'commands': []}
        func_pattern = '(?:export\\s+)?(?:async\\s+)?function\\s+(\\w+)'
        info['functions'] = re.findall(func_pattern, content)
        class_pattern = '(?:export\\s+)?class\\s+(\\w+)'
        info['classes'] = re.findall(class_pattern, content)
        import_pattern = 'import\\s+.*?\\s+from\\s+[\\\'"]([^\\\'"]+)[\\\'"]'
        info['imports'] = re.findall(import_pattern, content)
        export_pattern = 'export\\s+(?:default\\s+)?(?:class|function|const|let|var)?\\s*(\\w+)'
        info['exports'] = re.findall(export_pattern, content)
        command_pattern = '[\\\'"]([a-zA-Z]+\\.[a-zA-Z.]+)[\\\'"]'
        potential_commands = re.findall(command_pattern, content)
        info['commands'] = [cmd for cmd in potential_commands if 'deepseek' in cmd or 'command' in cmd.lower()]
        return info

    def _analyze_python_file(self: Any, content: str) -> dict[str, Any]:
        """Phân tích file Python"""
        info = {'functions': [], 'classes': [], 'imports': []}
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    info['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    info['classes'].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        info['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        info['imports'].append(node.module)
        except:
            func_pattern = 'def\\s+(\\w+)\\s*\\('
            info['functions'] = re.findall(func_pattern, content)
            class_pattern = 'class\\s+(\\w+)\\s*[:\\(]'
            info['classes'] = re.findall(class_pattern, content)
        return info

    def _analyze_json_file(self: Any, content: str) -> dict[str, Any]:
        """Phân tích file JSON"""
        info = {'keys': [], 'structure': {}}
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                info['keys'] = list(data.keys())
                info['structure'] = {'scripts': list(data.get('scripts', {}).keys()), 'dependencies': list(data.get('dependencies', {}).keys()), 'devDependencies': list(data.get('devDependencies', {}).keys()), 'commands': [cmd.get('command') for cmd in data.get('contributes', {}).get('commands', [])], 'activationEvents': data.get('activationEvents', [])}
        except:
            pass
        return info

    def _analyze_script_file(self: Any, content: str) -> dict[str, Any]:
        """Phân tích file script (.bat, .ps1)"""
        info = {'commands': [], 'environment_vars': []}
        if content.startswith('@echo off') or 'echo' in content:
            info['commands'] = re.findall('(\\w+\\.exe|\\w+\\s)', content)
        else:
            info['commands'] = re.findall('(\\w+-\\w+|\\w+\\.exe)', content)
        env_pattern = '\\$env:(\\w+)|%(\\w+)%|set\\s+(\\w+)='
        matches = re.findall(env_pattern, content)
        for match in matches:
            var_name = next(filter(None, match), None)
            if var_name:
                info['environment_vars'].append(var_name)
        return info

    def _analyze_dependencies(self: Any) -> Any:
        """Phân tích dependencies"""
        print('  📦 Phân tích dependencies...')
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, encoding='utf-8') as f:
                    package_data = json.load(f)
                self.integration_map['dependencies'] = {'npm': {'dependencies': package_data.get('dependencies', {}), 'devDependencies': package_data.get('devDependencies', {}), 'peerDependencies': package_data.get('peerDependencies', {}), 'scripts': package_data.get('scripts', {})}}
            except:
                pass
        requirements_file = self.project_root / 'requirements.txt'
        if requirements_file.exists():
            try:
                with open(requirements_file, encoding='utf-8') as f:
                    python_deps = [line.strip() for line in f if line.strip() and (not line.startswith('#'))]
                self.integration_map['dependencies']['python'] = {'requirements': python_deps}
            except:
                pass

    def _analyze_imports_exports(self: Any) -> Any:
        """Phân tích mối quan hệ imports/exports giữa các file"""
        print('  🔗 Phân tích imports/exports...')
        import_graph = {}
        for ts_file in self.project_root.rglob('*.ts'):
            if any(exclude in str(ts_file) for exclude in self.exclude_dirs):
                continue
            relative_path = ts_file.relative_to(self.project_root)
            import_graph[str(relative_path)] = {'imports': [], 'exports': [], 'internal_imports': [], 'external_imports': []}
            try:
                with open(ts_file, encoding='utf-8') as f:
                    content = f.read()
                import_pattern = 'import\\s+.*?\\s+from\\s+[\\\'"]([^\\\'"]+)[\\\'"]'
                imports = re.findall(import_pattern, content)
                for imp in imports:
                    import_graph[str(relative_path)]['imports'].append(imp)
                    if imp.startswith('.') or imp.startswith('/'):
                        import_graph[str(relative_path)]['internal_imports'].append(imp)
                    else:
                        import_graph[str(relative_path)]['external_imports'].append(imp)
                export_pattern = 'export\\s+(?:default\\s+)?(?:class|function|const|let|var)?\\s*(\\w+)'
                exports = re.findall(export_pattern, content)
                import_graph[str(relative_path)]['exports'] = exports
            except:
                pass
        self.integration_map['imports_exports'] = import_graph

    def _find_integration_points(self: Any) -> Any:
        """Tìm các điểm integration quan trọng"""
        print('  🎯 Tìm integration points...')
        integration_points = {'vscode_commands': [], 'ollama_integrations': [], 'file_dependencies': [], 'critical_paths': []}
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, encoding='utf-8') as f:
                    data = json.load(f)
                    commands = data.get('contributes', {}).get('commands', [])
                    integration_points['vscode_commands'] = [{'command': cmd.get('command'), 'title': cmd.get('title'), 'implementation': 'src/extension.ts'} for cmd in commands]
            except:
                pass
        for file_path, file_info in self.integration_map['core_files'].items():
            if 'ollama' in file_path.lower() or any('ollama' in imp.lower() for imp in file_info.get('imports', [])):
                integration_points['ollama_integrations'].append({'file': file_path, 'type': 'client' if 'client' in file_path else 'integration', 'functions': file_info.get('functions', [])})
        critical_files = ['src/extension.ts', 'src/aiAgent.ts', 'package.json']
        for file_path in critical_files:
            if file_path in self.integration_map['core_files']:
                file_info = self.integration_map['core_files'][file_path]
                integration_points['critical_paths'].append({'file': file_path, 'depends_on': file_info.get('imports', []), 'exports_to': file_info.get('exports', []), 'status': 'exists' if file_info['exists'] else 'missing'})
        self.integration_map['integration_points'] = integration_points

    def _analyze_build_flow(self: Any) -> Any:
        """Phân tích quy trình build"""
        print('  🔨 Phân tích build flow...')
        build_flow = {'steps': [], 'scripts': {}, 'configuration_files': [], 'output_paths': []}
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, encoding='utf-8') as f:
                    data = json.load(f)
                    scripts = data.get('scripts', {})
                build_flow['scripts'] = scripts
                if 'compile' in scripts:
                    build_flow['steps'].append('npm run compile')
                if 'build' in scripts:
                    build_flow['steps'].append('npm run build')
                if 'test' in scripts:
                    build_flow['steps'].append('npm run test')
                if 'package' in scripts:
                    build_flow['steps'].append('npm run package')
            except:
                pass
        config_files = ['tsconfig.json', '.eslintrc.json', 'jest.config.js']
        for config_file in config_files:
            config_path = self.project_root / config_file
            if config_path.exists():
                build_flow['configuration_files'].append(config_file)
        tsconfig_path = self.project_root / 'tsconfig.json'
        if tsconfig_path.exists():
            try:
                with open(tsconfig_path, encoding='utf-8') as f:
                    tsconfig = json.load(f)
                    out_dir = tsconfig.get('compilerOptions', {}).get('outDir', './out')
                    build_flow['output_paths'].append(out_dir)
            except:
                pass
        self.integration_map['build_flow'] = build_flow

    def _analyze_runtime_flow(self: Any) -> Any:
        """Phân tích quy trình runtime"""
        print('  ⚡ Phân tích runtime flow...')
        runtime_flow = {'activation_events': [], 'command_flow': {}, 'ai_agent_flow': [], 'external_dependencies': []}
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, encoding='utf-8') as f:
                    data = json.load(f)
                    runtime_flow['activation_events'] = data.get('activationEvents', [])
                    commands = data.get('contributes', {}).get('commands', [])
                    for cmd in commands:
                        cmd_id = cmd.get('command', '')
                        runtime_flow['command_flow'][cmd_id] = {'title': cmd.get('title', ''), 'handler': 'extension.ts', 'triggers': 'Command Palette / Keybinding'}
            except:
                pass
        runtime_flow['ai_agent_flow'] = ['User triggers command', 'extension.ts receives command', 'AIAgent.runTask() called', 'OllamaClient sends request to Ollama', 'AI model processes and returns plan', 'Actions applied to workspace', 'Results logged to Output Channel']
        runtime_flow['external_dependencies'] = ['Ollama server (http://127.0.0.1:11434)', 'DeepSeek-R1 model', 'VS Code API', 'Node.js fetch API']
        self.integration_map['runtime_flow'] = runtime_flow

    def _detect_issues_and_recommendations(self: Any) -> Any:
        """Phát hiện vấn đề và đưa ra khuyến nghị"""
        print('  🔍 Phát hiện issues và recommendations...')
        issues = []
        recommendations = []
        required_files = [('src/extension.ts', 'Main extension file'), ('package.json', 'Extension manifest'), ('tsconfig.json', 'TypeScript configuration')]
        for file_path, description in required_files:
            if file_path not in self.integration_map['core_files'] or not self.integration_map['core_files'][file_path]['exists']:
                issues.append(f'Missing {description}: {file_path}')
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, encoding='utf-8') as f:
                    data = json.load(f)
                commands = data.get('contributes', {}).get('commands', [])
                if not commands:
                    issues.append('No commands defined in package.json')
                activation_events = data.get('activationEvents', [])
                if not activation_events:
                    issues.append('No activation events defined')
                scripts = data.get('scripts', {})
                if 'compile' not in scripts:
                    recommendations.append("Add 'compile' script for TypeScript compilation")
                if 'test' not in scripts:
                    recommendations.append("Add 'test' script for running tests")
            except:
                issues.append('Invalid package.json format')
        if 'tsconfig.json' in self.integration_map['core_files']:
            recommendations.append('Ensure TypeScript compilation is working properly')
        ollama_files = [f for f in self.integration_map['core_files'] if 'ollama' in f.lower()]
        if not ollama_files:
            issues.append('No Ollama integration files found')
        recommendations.extend(['Use .env file for API keys instead of hardcoding', 'Add error handling for network requests', 'Implement proper logging for debugging', 'Add unit tests for core functionality', 'Consider adding CI/CD pipeline'])
        self.integration_map['issues'] = issues
        self.integration_map['recommendations'] = recommendations

    def generate_integration_report(self: Any, output_file: str='INTEGRATION_MAP.md') -> str:
        """Tạo báo cáo integration map dạng Markdown"""
        print(f'📝 Tạo báo cáo integration map: {output_file}')
        report = []
        report.append('# DEEPSEEK EXTENSION - INTEGRATION MAP')
        report.append(f"> Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append('')
        info = self.integration_map['project_info']
        report.append('## 📊 PROJECT OVERVIEW')
        report.append('')
        report.append(f"**Name:** {info['name']}")
        report.append(f"**Version:** {info['version']}")
        report.append(f"**Description:** {info['description']}")
        report.append(f"**Total Files:** {info['total_files']}")
        report.append(f"**Total Directories:** {info['total_directories']}")
        report.append('')
        report.append('### File Types Distribution')
        report.append('```')
        for ext, count in sorted(info['file_types'].items()):
            report.append(f'{ext:<10} : {count:>3} files')
        report.append('```')
        report.append('')
        report.append('## 🎯 CORE FILES ANALYSIS')
        report.append('')
        for file_path, file_info in self.integration_map['core_files'].items():
            status = '✅' if file_info['exists'] else '❌'
            report.append(f'### {status} {file_path}')
            report.append(f"**Purpose:** {file_info['description']}")
            if file_info['exists']:
                report.append(f"**Size:** {file_info['size']:,} bytes")
                report.append(f"**Lines:** {file_info.get('lines', 0)}")
                if file_info.get('functions'):
                    report.append(f"**Functions:** {', '.join(file_info['functions'])}")
                if file_info.get('classes'):
                    report.append(f"**Classes:** {', '.join(file_info['classes'])}")
                if file_info.get('imports'):
                    report.append(f"**Imports:** {', '.join(file_info['imports'][:5])}")
                    if len(file_info['imports']) > 5:
                        report.append(f" ... and {len(file_info['imports']) - 5} more")
                if file_info.get('commands'):
                    report.append(f"**Commands:** {', '.join(file_info['commands'])}")
            else:
                report.append('**Status:** MISSING ⚠️')
            report.append('')
        report.append('## 📦 DEPENDENCIES')
        report.append('')
        deps = self.integration_map.get('dependencies', {})
        if 'npm' in deps:
            npm_deps = deps['npm']
            report.append('### NPM Dependencies')
            if npm_deps.get('dependencies'):
                report.append('**Runtime Dependencies:**')
                for pkg, version in npm_deps['dependencies'].items():
                    report.append(f'- {pkg}: {version}')
                report.append('')
            if npm_deps.get('devDependencies'):
                report.append('**Development Dependencies:**')
                for pkg, version in npm_deps['devDependencies'].items():
                    report.append(f'- {pkg}: {version}')
                report.append('')
            if npm_deps.get('scripts'):
                report.append('**NPM Scripts:**')
                for script, command in npm_deps['scripts'].items():
                    report.append(f'- `{script}`: {command}')
                report.append('')
        if 'python' in deps:
            python_deps = deps['python']
            report.append('### Python Dependencies')
            for req in python_deps.get('requirements', []):
                report.append(f'- {req}')
            report.append('')
        report.append('## 🔗 INTEGRATION POINTS')
        report.append('')
        integration_points = self.integration_map.get('integration_points', {})
        if integration_points.get('vscode_commands'):
            report.append('### VS Code Commands')
            report.append('| Command ID | Title | Implementation |')
            report.append('|------------|-------|----------------|')
            for cmd in integration_points['vscode_commands']:
                report.append(f"| `{cmd['command']}` | {cmd['title']} | {cmd['implementation']} |")
            report.append('')
        if integration_points.get('ollama_integrations'):
            report.append('### Ollama Integrations')
            for integration in integration_points['ollama_integrations']:
                report.append(f"- **{integration['file']}** ({integration['type']})")
                if integration.get('functions'):
                    report.append(f"  - Functions: {', '.join(integration['functions'])}")
            report.append('')
        if integration_points.get('critical_paths'):
            report.append('### Critical Dependency Paths')
            for path in integration_points['critical_paths']:
                status = '✅' if path['status'] == 'exists' else '❌'
                report.append(f"- {status} **{path['file']}**")
                if path.get('depends_on'):
                    report.append(f"  - Imports: {', '.join(path['depends_on'][:3])}")
                if path.get('exports_to'):
                    report.append(f"  - Exports: {', '.join(path['exports_to'][:3])}")
            report.append('')
        report.append('## 🔨 BUILD FLOW')
        report.append('')
        build_flow = self.integration_map.get('build_flow', {})
        if build_flow.get('steps'):
            report.append('### Build Steps')
            for i, step in enumerate(build_flow['steps'], 1):
                report.append(f'{i}. `{step}`')
            report.append('')
        if build_flow.get('configuration_files'):
            report.append('### Configuration Files')
            for config_file in build_flow['configuration_files']:
                report.append(f'- ✅ {config_file}')
            report.append('')
        report.append('## ⚡ RUNTIME FLOW')
        report.append('')
        runtime_flow = self.integration_map.get('runtime_flow', {})
        if runtime_flow.get('ai_agent_flow'):
            report.append('### AI Agent Execution Flow')
            for i, step in enumerate(runtime_flow['ai_agent_flow'], 1):
                report.append(f'{i}. {step}')
            report.append('')
        if runtime_flow.get('external_dependencies'):
            report.append('### External Dependencies')
            for dep in runtime_flow['external_dependencies']:
                report.append(f'- {dep}')
            report.append('')
        issues = self.integration_map.get('issues', [])
        if issues:
            report.append('## ⚠️ ISSUES DETECTED')
            report.append('')
            for issue in issues:
                report.append(f'- ❌ {issue}')
            report.append('')
        recommendations = self.integration_map.get('recommendations', [])
        if recommendations:
            report.append('## 💡 RECOMMENDATIONS')
            report.append('')
            for rec in recommendations:
                report.append(f'- 💡 {rec}')
            report.append('')
        report.append('---')
        report.append('*Generated by DeepSeek Extension Integration Mapper*')
        report.append(f"*Project Root: {self.integration_map['project_info']['project_root']}*")
        output_path = self.project_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        return str(output_path)

    def generate_json_report(self: Any, output_file: str='integration_map.json') -> str:
        """Tạo báo cáo dạng JSON để xử lý programmatically"""
        output_path = self.project_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.integration_map, f, indent=2, ensure_ascii=False)
        return str(output_path)

def main() -> Any:
    """Main function"""
    import argparse
    parser = argparse.ArgumentParser(description='DeepSeek Extension Integration Mapper')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--output-md', default='INTEGRATION_MAP.md', help='Markdown output file')
    parser.add_argument('--output-json', default='integration_map.json', help='JSON output file')
    parser.add_argument('--json-only', action='store_true', help='Generate only JSON output')
    parser.add_argument('--preview', action='store_true', help='Preview integration info in console')
    args = parser.parse_args()
    print('🎯 DEEPSEEK EXTENSION - INTEGRATION MAPPER')
    print('=' * 50)
    mapper = IntegrationMapper(args.project_root)
    integration_map = mapper.analyze_project()
    if args.preview:
        print('\n📊 INTEGRATION OVERVIEW:')
        info = integration_map['project_info']
        print(f"   Project: {info['name']} v{info['version']}")
        print(f"   Files: {info['total_files']}")
        print(f"   Directories: {info['total_directories']}")
        print('\n🎯 CORE FILES STATUS:')
        for file_path, file_info in integration_map['core_files'].items():
            status = '✅' if file_info['exists'] else '❌'
            print(f'   {status} {file_path}')
        issues = integration_map.get('issues', [])
        if issues:
            print(f'\n⚠️  ISSUES FOUND: {len(issues)}')
            for issue in issues[:3]:
                print(f'   - {issue}')
            if len(issues) > 3:
                print(f'   ... and {len(issues) - 3} more')
    if not args.json_only:
        md_file = mapper.generate_integration_report(args.output_md)
        print(f'\n✅ Markdown report: {md_file}')
    json_file = mapper.generate_json_report(args.output_json)
    print(f'✅ JSON report: {json_file}')
    print('\n🎉 Integration mapping completed!')
if __name__ == '__main__':
    main()
