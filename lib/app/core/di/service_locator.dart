import 'dart:async';
import 'dart:convert';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:shared_preferences/shared_preferences.dart';

// core
import '../utils/app_constants.dart';
import '../themes/theme_cubit.dart';

// auth
import '../../features/auth/data/datasources/auth_local_data_source.dart';
import '../../features/auth/data/datasources/auth_remote_data_source.dart';
import '../../features/auth/data/repositories/auth_repository_impl.dart';
import '../../features/auth/domain/repositories/auth_repository.dart';
import '../../features/auth/domain/usecases/auth_usecase.dart';
import '../../features/auth/presentation/bloc/auth_bloc.dart';
import '../../features/auth/presentation/bloc/auth_event.dart';

// category
import '../../features/category/data/datasources/category_remote_data_source.dart';
import '../../features/category/data/datasources/category_local_data_source.dart';
import '../../features/category/data/repositories/category_repository_impl.dart';
import '../../features/category/domain/repositories/category_repository.dart';
import '../../features/category/domain/usecases/category_usecases.dart';
import '../../features/category/presentation/bloc/category_bloc.dart';

// quiz
import '../../features/quiz/data/datasources/quiz_remote_data_source.dart';
import '../../features/quiz/data/datasources/quiz_local_data_source.dart';
import '../../features/quiz/data/repositories/quiz_repository_impl.dart';
import '../../features/quiz/domain/repositories/quiz_repository.dart';
import '../../features/quiz/domain/usecases/quiz_usecases.dart'
    as quiz_usecases;
import '../../features/quiz/presentation/bloc/quiz_bloc.dart';

// attempts
import '../../features/attempts/data/datasources/attempts_remote_datasource.dart';
import '../../features/attempts/data/datasources/attempts_local_datasource.dart';
import '../../features/attempts/data/repositories/attempts_repository_impl.dart';
import '../../features/attempts/domain/repositories/attempts_repository.dart';
import '../../features/attempts/domain/usecases/attempts_usecases.dart'
    as attempt_usecases;
import '../../features/attempts/presentation/bloc/attempts_bloc.dart';

// user_stats
import '../../features/user_stats/data/datasources/user_stats_remote_datasource.dart';
import '../../features/user_stats/data/datasources/user_stats_local_datasource.dart';
import '../../features/user_stats/data/repositories/user_stats_repository_impl.dart';
import '../../features/user_stats/domain/repositories/user_stats_repository.dart';
import '../../features/user_stats/domain/usecases/get_user_progression_usecase.dart';
import '../../features/user_stats/presentation/bloc/user_stats_bloc.dart';

final sl = GetIt.instance;

/// NetworkInfo
abstract class NetworkInfo {
  Future<bool> get isConnected;
  Stream<bool> get onConnectivityChanged;
  Future<void> initialize();
  void dispose();
}

/// Implementation using connectivity_plus V4.0.2
class NetworkInfoImpl implements NetworkInfo {
  final Connectivity _connectivity;
  StreamSubscription<ConnectivityResult>? _sub;
  final StreamController<bool> _controller = StreamController<bool>.broadcast();

  NetworkInfoImpl({Connectivity? connectivity})
      : _connectivity = connectivity ?? Connectivity();

  @override
  Future<bool> get isConnected async {
    final result = await _connectivity.checkConnectivity();
    return result != ConnectivityResult.none;
  }

  @override
  Stream<bool> get onConnectivityChanged => _controller.stream;

  @override
  Future<void> initialize() async {
    final initial = await isConnected;
    _controller.add(initial);

    _sub = _connectivity.onConnectivityChanged.listen((result) async {
      final connected = result != ConnectivityResult.none;
      _controller.add(connected);

      if (connected) {
        try {
          if (sl.isRegistered<QuizRepository>()) {
            final repo = sl<QuizRepository>();
            await repo.flushPendingSubmissions();
          }
        } catch (_) {
          // Ignorer les erreurs de flush
        }
      }
    });
  }

  @override
  void dispose() {
    _sub?.cancel();
    _controller.close();
  }
}

/// Custom Interceptor for intelligent logging
class IntelligentLoggingInterceptor extends Interceptor {
  static const int _maxBodyLength = 2000;
  static const int _maxHeadersLength = 1000;

  final bool logInRelease;
  final bool showSensitiveData;
  final Set<String> sensitiveEndpoints = {
    '/auth/login',
    '/auth/register',
    '/auth/token',
    '/users/password',
  };

  IntelligentLoggingInterceptor({
    this.logInRelease = false,
    this.showSensitiveData = false,
  });

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (!_shouldLog()) return super.onRequest(options, handler);
    options.extra['start_time'] = DateTime.now();
    _logRequest(options);
    return super.onRequest(options, handler);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    if (!_shouldLog()) return super.onResponse(response, handler);
    final startTime = response.requestOptions.extra['start_time'] as DateTime?;
    final duration =
        startTime != null ? DateTime.now().difference(startTime) : null;
    _logResponse(response, duration);
    return super.onResponse(response, handler);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (!_shouldLog()) return super.onError(err, handler);
    final startTime = err.requestOptions.extra['start_time'] as DateTime?;
    final duration =
        startTime != null ? DateTime.now().difference(startTime) : null;
    _logError(err, duration);
    return super.onError(err, handler);
  }

  bool _shouldLog() {
    const bool isReleaseMode = bool.fromEnvironment('dart.vm.product');
    return !isReleaseMode || logInRelease;
  }

  void _logRequest(RequestOptions options) {
    final buffer = StringBuffer();
    buffer.writeln('┌── HTTP REQUEST ───────────────────────────────────────');
    buffer.writeln('│ 📤 ${options.method.toUpperCase()} ${options.uri}');
    if (options.headers.isNotEmpty) {
      buffer.writeln('├─ Headers ──────────────────────────────────────────');
      _logHeaders(options.headers, buffer);
    }
    if (options.data != null && _shouldLogBody(options.uri.toString())) {
      buffer.writeln('├─ Body ─────────────────────────────────────────────');
      _logBody(options.data, buffer);
    }
    buffer.writeln('└──────────────────────────────────────────────────────');
    debugPrint(buffer.toString());
  }

  void _logResponse(Response response, Duration? duration) {
    final buffer = StringBuffer();
    final statusCode = response.statusCode ?? 0;
    final statusEmoji = _getStatusCodeEmoji(statusCode);
    final durationStr =
        duration != null ? ' (${duration.inMilliseconds}ms)' : '';
    buffer.writeln('┌── HTTP RESPONSE ──────────────────────────────────────');
    buffer.writeln(
        '│ 📥 $statusEmoji ${response.requestOptions.method.toUpperCase()} '
        '${response.requestOptions.uri} → $statusCode$durationStr');
    if (!response.headers.isEmpty) {
      buffer.writeln('├─ Headers ──────────────────────────────────────────');
      _logHeaders(response.headers.map, buffer);
    }
    if (response.data != null &&
        _shouldLogBody(response.requestOptions.uri.toString())) {
      buffer.writeln('├─ Body ─────────────────────────────────────────────');
      _logBody(response.data, buffer);
    }
    buffer.writeln('└──────────────────────────────────────────────────────');
    debugPrint(buffer.toString());
  }

  void _logError(DioException err, Duration? duration) {
    final buffer = StringBuffer();
    final statusCode = err.response?.statusCode ?? 0;
    final statusEmoji = _getStatusCodeEmoji(statusCode);
    final durationStr =
        duration != null ? ' (${duration.inMilliseconds}ms)' : '';
    buffer.writeln('┌── HTTP ERROR ─────────────────────────────────────────');
    buffer
        .writeln('│ ❌ $statusEmoji ${err.requestOptions.method.toUpperCase()} '
            '${err.requestOptions.uri} → $statusCode$durationStr');
    buffer.writeln('├─ Error Type ────────────────────────────────────────');
    buffer.writeln('│ ${err.type}');
    if (err.response != null) {
      if (!err.response!.headers.isEmpty) {
        buffer.writeln('├─ Headers ──────────────────────────────────────────');
        _logHeaders(err.response!.headers.map, buffer);
      }
      if (err.response!.data != null) {
        buffer.writeln('├─ Error Body ───────────────────────────────────────');
        _logBody(err.response!.data, buffer);
      }
    }
    if (err.error != null) {
      buffer.writeln('├─ Original Error ────────────────────────────────────');
      buffer.writeln('│ ${err.error}');
    }
    buffer.writeln('└──────────────────────────────────────────────────────');
    debugPrint(buffer.toString());
  }

  void _logHeaders(Map<String, dynamic> headers, StringBuffer buffer) {
    final headerString = headers.entries.take(10).map((e) {
      final key = e.key;
      var value = e.value.toString();
      if (!showSensitiveData &&
          (key.toLowerCase().contains('authorization') ||
              key.toLowerCase().contains('token') ||
              key.toLowerCase().contains('cookie'))) {
        value = '***HIDDEN***';
      }
      return '$key: $value';
    }).join('\n│ ');
    final displayString = headerString.length > _maxHeadersLength
        ? '${headerString.substring(0, _maxHeadersLength)}...'
        : headerString;
    buffer.writeln('│ $displayString');
  }

  void _logBody(dynamic body, StringBuffer buffer) {
    String bodyString;
    try {
      if (body is Map || body is List) {
        bodyString = const JsonEncoder.withIndent('  ').convert(body);
      } else if (body is String) {
        try {
          final jsonObj = jsonDecode(body);
          bodyString = const JsonEncoder.withIndent('  ').convert(jsonObj);
        } catch (_) {
          bodyString = body;
        }
      } else {
        bodyString = body.toString();
      }
      bodyString = bodyString.length > _maxBodyLength
          ? '${bodyString.substring(0, _maxBodyLength)}...\n│ [Truncated - ${bodyString.length} chars total]'
          : bodyString;
      final lines = bodyString.split('\n');
      for (final line in lines) {
        buffer.writeln('│ $line');
      }
    } catch (e) {
      buffer.writeln('│ [Unable to format body: $e]');
    }
  }

  String _getStatusCodeEmoji(int code) {
    if (code >= 200 && code < 300) return '✅';
    if (code >= 300 && code < 400) return '↪️';
    if (code >= 400 && code < 500) return '⚠️';
    if (code >= 500) return '🔥';
    return '❓';
  }

  bool _shouldLogBody(String uri) {
    if (!showSensitiveData) {
      return !sensitiveEndpoints.any((endpoint) => uri.contains(endpoint));
    }
    return true;
  }
}

/// Performance tracking interceptor
class PerformanceInterceptor extends Interceptor {
  final Map<String, List<Duration>> _timings = {};
  static const int _maxTimingsPerEndpoint = 10;

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    options.extra['start_time'] = DateTime.now();
    return super.onRequest(options, handler);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    final startTime = response.requestOptions.extra['start_time'] as DateTime?;
    if (startTime != null) {
      final duration = DateTime.now().difference(startTime);
      final endpoint = response.requestOptions.uri.path;
      _timings[endpoint] = _timings[endpoint] ?? [];
      _timings[endpoint]!.add(duration);
      if (_timings[endpoint]!.length > _maxTimingsPerEndpoint) {
        _timings[endpoint]!.removeAt(0);
      }
      if (duration.inMilliseconds > 1000) {
        final avgDuration = _getAverageDuration(endpoint);
        debugPrint(
            '⚠️ Slow request: ${response.requestOptions.uri.path} took ${duration.inMilliseconds}ms '
            '(avg: ${avgDuration?.inMilliseconds ?? 0}ms)');
      }
    }
    return super.onResponse(response, handler);
  }

  Duration? _getAverageDuration(String endpoint) {
    final timings = _timings[endpoint];
    if (timings == null || timings.isEmpty) return null;
    final totalMicroseconds =
        timings.fold<int>(0, (sum, duration) => sum + duration.inMicroseconds);
    return Duration(microseconds: totalMicroseconds ~/ timings.length);
  }
}

/// Crée et configure l'instance Dio
Dio _createDio() {
  final dio = Dio(
    BaseOptions(
      baseUrl: AppConstants.baseUrl,
      connectTimeout: AppConstants.connectTimeout,
      receiveTimeout: AppConstants.receiveTimeout,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ),
  );

  // Ajouter les intercepteurs
  dio.interceptors.addAll([
    IntelligentLoggingInterceptor(
      logInRelease: false,
      showSensitiveData: false,
    ),
    PerformanceInterceptor(),
  ]);

  // Intercepteur pour ajouter le token automatiquement
  dio.interceptors.add(
    InterceptorsWrapper(
      onRequest: (options, handler) async {
        try {
          if (sl.isRegistered<AuthLocalDataSource>()) {
            final authLocal = sl<AuthLocalDataSource>();
            final token = await authLocal.getToken();
            if (token != null && token.isNotEmpty) {
              options.headers['Authorization'] = 'Bearer $token';
            }
          }
        } catch (_) {
          // Ignorer les erreurs
        }
        return handler.next(options);
      },
      onError: (error, handler) async {
        // Auto-logout sur 401
        if (error.response?.statusCode == 401) {
          try {
            if (sl.isRegistered<AuthBloc>()) {
              sl<AuthBloc>().add(const AutoLogoutTriggered());
            }
          } catch (_) {
            // Ignorer
          }
        }
        return handler.next(error);
      },
    ),
  );

  return dio;
}

/// Initialise toutes les dépendances
Future<void> initializeDependencies() async {
  // ============================================================================
  // EXTERNAL
  // ============================================================================
  final sharedPreferences = await SharedPreferences.getInstance();
  sl.registerSingleton<SharedPreferences>(sharedPreferences);
  sl.registerSingleton<GlobalKey<NavigatorState>>(GlobalKey<NavigatorState>());
  sl.registerSingleton<Dio>(_createDio());

  // ============================================================================
  // CORE
  // ============================================================================
  final networkInfo = NetworkInfoImpl();
  await networkInfo.initialize();
  sl.registerSingleton<NetworkInfo>(networkInfo);
  sl.registerSingleton<ThemeCubit>(ThemeCubit(sharedPreferences));

  // ============================================================================
  // AUTH
  // ============================================================================
  sl.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSourceImpl(sl<Dio>()),
  );

  sl.registerLazySingleton<AuthLocalDataSource>(
    () => AuthLocalDataSourceImpl(sl<SharedPreferences>()),
  );

  sl.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      remoteDataSource: sl<AuthRemoteDataSource>(),
      localDataSource: sl<AuthLocalDataSource>(),
    ),
  );

  // Use Cases
  sl.registerLazySingleton(() => LoginUseCase(sl<AuthRepository>()));
  sl.registerLazySingleton(() => RegisterUseCase(sl<AuthRepository>()));
  sl.registerLazySingleton(() => LogoutUseCase(sl<AuthRepository>()));
  sl.registerLazySingleton(() => GetCurrentUserUseCase(sl<AuthRepository>()));
  sl.registerLazySingleton(
      () => CheckAuthenticationUseCase(sl<AuthRepository>()));
  sl.registerLazySingleton(() => GetTokenUseCase(sl<AuthRepository>()));

  // Bloc
  sl.registerLazySingleton(
    () => AuthBloc(
      loginUseCase: sl<LoginUseCase>(),
      registerUseCase: sl<RegisterUseCase>(),
      logoutUseCase: sl<LogoutUseCase>(),
      getCurrentUserUseCase: sl<GetCurrentUserUseCase>(),
      checkAuthenticationUseCase: sl<CheckAuthenticationUseCase>(),
    ),
  );

  // ============================================================================
  // CATEGORY
  // ============================================================================
  sl.registerLazySingleton<CategoryRemoteDataSource>(
    () => CategoryRemoteDataSourceImpl(sl<Dio>()),
  );

  sl.registerLazySingleton<CategoryLocalDataSource>(
    () => CategoryLocalDataSourceImpl(sl<SharedPreferences>()),
  );

  sl.registerLazySingleton<CategoryRepository>(
    () => CategoryRepositoryImpl(
      remoteDataSource: sl<CategoryRemoteDataSource>(),
      localDataSource: sl<CategoryLocalDataSource>(),
    ),
  );

  // Use Cases
  sl.registerLazySingleton(
      () => GetCategoriesUseCase(sl<CategoryRepository>()));
  sl.registerLazySingleton(
      () => GetCategoryByIdUseCase(sl<CategoryRepository>()));

  sl.registerFactory(
    () => CategoryBloc(
      getCategoriesUseCase: sl<GetCategoriesUseCase>(),
      getCategoryByIdUseCase: sl<GetCategoryByIdUseCase>(),
      remoteDataSource: sl<CategoryRemoteDataSource>(),
    ),
  );

  // ============================================================================
  // QUIZ
  // ============================================================================
  sl.registerLazySingleton<QuizRemoteDataSource>(
    () => QuizRemoteDataSourceImpl(sl<Dio>()),
  );

  sl.registerLazySingleton<QuizLocalDataSource>(
    () => QuizLocalDataSourceImpl(sl<SharedPreferences>()),
  );

  sl.registerLazySingleton<QuizRepository>(
    () => QuizRepositoryImpl(
      remoteDataSource: sl<QuizRemoteDataSource>(),
      localDataSource: sl<QuizLocalDataSource>(),
      authLocalDataSource: sl<AuthLocalDataSource>(),
      networkInfo: sl<NetworkInfo>(),
    ),
  );

  // Use Cases
  sl.registerLazySingleton(
      () => quiz_usecases.GetQuizByIdUseCase(sl<QuizRepository>()));
  sl.registerLazySingleton(
      () => quiz_usecases.GetAvailableQuizzesUseCase(sl<QuizRepository>()));
  sl.registerLazySingleton(
      () => quiz_usecases.StartQuizUseCase(sl<QuizRepository>()));
  sl.registerLazySingleton(
      () => quiz_usecases.SubmitQuizUseCase(sl<QuizRepository>()));
  sl.registerLazySingleton(
      () => quiz_usecases.GetAttemptByIdUseCase(sl<QuizRepository>()));
  sl.registerLazySingleton(
      () => quiz_usecases.GetUserAttemptsUseCase(sl<QuizRepository>()));
  sl.registerLazySingleton(
      () => quiz_usecases.FlushPendingSubmissionsUseCase(sl<QuizRepository>()));

  // Bloc
  sl.registerFactory(
    () => QuizBloc(
      getQuizByIdUseCase: sl<quiz_usecases.GetQuizByIdUseCase>(),
      startQuizUseCase: sl<quiz_usecases.StartQuizUseCase>(),
      submitQuizUseCase: sl<quiz_usecases.SubmitQuizUseCase>(),
      flushPendingUseCase: sl<quiz_usecases.FlushPendingSubmissionsUseCase>(),
      localDataSource: sl<QuizLocalDataSource>(),
      remoteDataSource: sl<QuizRemoteDataSource>(),
    ),
  );

// ============================================================================
// ATTEMPTS
// ============================================================================
  sl.registerLazySingleton<AttemptsRemoteDataSource>(
    () => AttemptsRemoteDataSourceImpl(sl<Dio>()),
  );

  sl.registerLazySingleton<AttemptsLocalDataSource>(
    () => AttemptsLocalDataSourceImpl(sl<SharedPreferences>()),
  );

  sl.registerLazySingleton<AttemptsRepository>(
    () => AttemptsRepositoryImpl(
      remoteDataSource: sl<AttemptsRemoteDataSource>(),
      localDataSource: sl<AttemptsLocalDataSource>(),
    ),
  );

// Use Cases
  sl.registerLazySingleton(
      () => attempt_usecases.GetUserAttemptsUseCase(sl<AttemptsRepository>()));
  sl.registerLazySingleton(() =>
      attempt_usecases.GetAttemptStatisticsUseCase(sl<AttemptsRepository>()));

// Bloc - SINGLETON pour partager l'état entre les pages
  sl.registerLazySingleton(
    () => AttemptsBloc(
      getUserAttemptsUseCase: sl<attempt_usecases.GetUserAttemptsUseCase>(),
      getAttemptStatisticsUseCase:
          sl<attempt_usecases.GetAttemptStatisticsUseCase>(),
    ),
  );

// ============================================================================
// USER STATS
// ============================================================================
  sl.registerLazySingleton<UserStatsRemoteDataSource>(
    () => UserStatsRemoteDataSourceImpl(sl<Dio>()),
  );

  sl.registerLazySingleton<UserStatsLocalDataSource>(
    () => UserStatsLocalDataSourceImpl(sl<SharedPreferences>()),
  );

  sl.registerLazySingleton<UserStatsRepository>(
    () => UserStatsRepositoryImpl(
      remoteDataSource: sl<UserStatsRemoteDataSource>(),
      localDataSource: sl<UserStatsLocalDataSource>(),
    ),
  );

// Use Cases
  sl.registerLazySingleton(
      () => GetUserProgressionUseCase(sl<UserStatsRepository>()));

// Bloc - SINGLETON pour partager l'état entre les pages
  sl.registerLazySingleton(
    () => UserStatsBloc(
      getUserProgressionUseCase: sl<GetUserProgressionUseCase>(),
    ),
  );
}
