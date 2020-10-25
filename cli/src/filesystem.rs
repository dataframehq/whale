use std::path::Path;
use std::{
    collections::BTreeSet,
    env,
    fs::{self, OpenOptions},
    io::{BufWriter, Write},
};

pub fn create_file_structure() {
    let subdirs = [
        get_bin_dirname(),
        get_config_dirname(),
        get_libexec_dirname(),
        get_logs_dirname(),
        get_metadata_dirname(),
        get_manifest_dirname(),
        get_metrics_dirname(),
    ];

    for subdir in subdirs.iter() {
        fs::create_dir_all(Path::new(&*subdir)).expect("Directory was not created succesfully.");
    }
}

pub fn deduplicate_file(file_path_string: &str) {
    let file_path = Path::new(file_path_string);
    let contents = fs::read_to_string(file_path)
        .unwrap_or_else(|_| panic!("Can't read file `{}`", file_path_string));
    let lines: BTreeSet<_> = contents.lines().collect();
    match OpenOptions::new()
        .create(true)
        .write(true)
        .truncate(true)
        .open(&file_path_string)
    {
        Ok(file) => {
            let mut writer = BufWriter::new(&file);
            for line in lines {
                writeln!(writer, "{}", line).unwrap();
            }
            writer
                .flush()
                .unwrap_or_else(|_| panic!("Unable to write to file `{}`", file_path_string))
        }
        Err(err) => panic!("Failed to open file: {}", err),
    }
}

pub fn append_to_file(contents: String, path: &str) {
    let mut file = OpenOptions::new()
        .create(true)
        .write(true)
        .append(true)
        .open(path)
        .unwrap_or_else(|_| panic!("Failed to open file `{}`", path));
    writeln!(file, "{}", contents).unwrap_or_else(|_| panic!("Failed to write to file `{}`", path));
}

pub fn get_open_command() -> std::string::String {
    match std::env::var("EDITOR") {
        Ok(val) => val,
        Err(_) => "open".to_string(),
    }
}

pub fn get_etl_command() -> std::string::String {
    let path = format!("{}/{}/{}", get_base_dirname(), "bin", "whale");
    if Path::new(&*path).exists() {
        format!("{} pull", path)
    } else {
        "wh pull".to_string()
    }
}

pub fn get_libexec_dirname() -> std::string::String {
    let executable = env::current_exe().unwrap();
    let executable = std::fs::canonicalize(executable).unwrap();
    let path = match executable.parent() {
        Some(name) => name,
        _ => panic!(),
    };
    format!("{}/../{}", path.display(), "libexec")
}

pub fn get_activate_filename() -> std::string::String {
    format!("{}/{}", get_libexec_dirname(), "env/bin/activate")
}

pub fn get_base_dirname() -> std::string::String {
    shellexpand::tilde("~/.whale").into_owned()
}

pub fn get_bin_dirname() -> std::string::String {
    format!("{}/{}", get_base_dirname(), "bin")
}

pub fn get_build_script_filename() -> std::string::String {
    format!("{}/{}", get_libexec_dirname(), "build_script.py")
}

pub fn get_config_dirname() -> std::string::String {
    format!("{}/{}", get_base_dirname(), "config")
}

pub fn get_config_filename() -> std::string::String {
    format!("{}/{}", get_config_dirname(), "config.yaml")
}

pub fn get_connections_filename() -> std::string::String {
    format!("{}/{}", get_config_dirname(), "connections.yaml")
}

pub fn get_cron_log_filename() -> std::string::String {
    format!("{}/{}", get_logs_dirname(), "cron.log")
}

pub fn get_logs_dirname() -> std::string::String {
    format!("{}/{}", get_base_dirname(), "logs")
}

pub fn get_manifest_dirname() -> std::string::String {
    format!("{}/{}", get_base_dirname(), "manifests")
}

pub fn get_manifest_filename() -> std::string::String {
    format!("{}/{}", get_manifest_dirname(), "manifest.txt")
}

pub fn get_metadata_dirname() -> std::string::String {
    format!("{}/{}", get_base_dirname(), "metadata")
}

pub fn get_metrics_dirname() -> std::string::String {
    format!("{}/{}", get_base_dirname(), "metrics")
}

pub fn get_tmp_manifest_filename() -> std::string::String {
    format!("{}/{}", get_manifest_dirname(), "tmp_manifest.txt")
}

pub fn get_recently_used_filename() -> std::string::String {
    format!("{}/{}", get_logs_dirname(), "recently_used.txt")
}

pub fn get_run_script_filename() -> std::string::String {
    format!("{}/{}", get_libexec_dirname(), "run_script.py")
}

pub fn get_usage_filename() -> std::string::String {
    format!("{}/{}", get_logs_dirname(), "usage.csv")
}
