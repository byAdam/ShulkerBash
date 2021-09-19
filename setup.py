from cx_Freeze import setup, Executable

bdist_msi_options = {
    'upgrade_code': '{5fa7309a-bb70-42bb-bb83-6b1ee24f5026}',
    'add_to_path': True,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % ("shulker")
    }

build_exe_options = {
    'packages': ['shulker', 'shulker.commands'],
    'includes': ['atexit'],
    'include_files': ["pack/"]
    }

target = Executable(
    "shulker.py",
    icon="icon.ico",
    target_name="shulker.exe"
    )

setup(name = "Shulker Bash" ,
    version = "1.0.0",
    description = "A Bedrock mcfunction shell and interpreter" ,
    executables = [target],
    options={
        'bdist_msi': bdist_msi_options,
        'build_exe': build_exe_options})