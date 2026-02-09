import '../../domain/usecases/auth_usecase.dart';
import 'auth_event.dart';
import 'auth_state.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'dart:async';

/// Bloc pour gérer l'authentification
///
/// Responsabilités:
/// - Écouter les events (LoginRequested, etc.)
/// - Appeler les use cases
/// - Émettre les states (Authenticated, AuthError, etc.)
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUseCase _loginUseCase;
  final RegisterUseCase _registerUseCase;
  final LogoutUseCase _logoutUseCase;
  final GetCurrentUserUseCase _getCurrentUserUseCase;
  final CheckAuthenticationUseCase _checkAuthenticationUseCase;
  Timer? _authCheckTimeout;

  AuthBloc({
    required LoginUseCase loginUseCase,
    required RegisterUseCase registerUseCase,
    required LogoutUseCase logoutUseCase,
    required GetCurrentUserUseCase getCurrentUserUseCase,
    required CheckAuthenticationUseCase checkAuthenticationUseCase,
  })  : _loginUseCase = loginUseCase,
        _registerUseCase = registerUseCase,
        _logoutUseCase = logoutUseCase,
        _getCurrentUserUseCase = getCurrentUserUseCase,
        _checkAuthenticationUseCase = checkAuthenticationUseCase,
        super(const AuthInitial()) {
    // Enregistrer les handlers pour chaque event
    on<LoginRequested>(_onLoginRequested);
    on<RegisterRequested>(_onRegisterRequested);
    on<LogoutRequested>(_onLogoutRequested);
    on<AuthCheckRequested>(_onAuthCheckRequested);
    on<AutoLogoutTriggered>(_onAutoLogoutTriggered);
  }

  @override
  Future<void> close() {
    _authCheckTimeout?.cancel();
    return super.close();
  }

  // ==========================================================================
  // LOGIN
  // ==========================================================================

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(const AuthLoading());

    final result = await _loginUseCase(
      LoginParams(
        email: event.email,
        password: event.password,
      ),
    );

    result.fold(
      // Échec
      (failure) => emit(AuthError(failure.message)),
      // Succès
      (data) {
        final (user, token) = data;
        emit(Authenticated(user: user, token: token));
      },
    );
  }

  // ==========================================================================
  // REGISTER
  // ==========================================================================

  Future<void> _onRegisterRequested(
    RegisterRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(const AuthLoading());

    final result = await _registerUseCase(
      RegisterParams(
        name: event.name,
        email: event.email,
        password: event.password,
      ),
    );

    result.fold(
      (failure) => emit(AuthError(failure.message)),
      (data) {
        final (user, token) = data;
        emit(Authenticated(user: user, token: token));
      },
    );
  }

  // ==========================================================================
  // LOGOUT
  // ==========================================================================

  Future<void> _onLogoutRequested(
    LogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(const AuthLoading());

    final result = await _logoutUseCase();

    result.fold(
      (failure) => emit(AuthError(failure.message)),
      (_) => emit(const Unauthenticated()),
    );
  }

  // ==========================================================================
  // CHECK AUTH (au démarrage)
  // ==========================================================================

  Future<void> _onAuthCheckRequested(
    AuthCheckRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(const AuthChecking());

    // Timeout de sécurité (5 secondes max)
    _authCheckTimeout = Timer(const Duration(seconds: 5), () {
      if (state is AuthChecking) {
        emit(const Unauthenticated());
      }
    });

    try {
      // Vérifier si un token existe
      final isAuth = await _checkAuthenticationUseCase();

      if (!isAuth) {
        _authCheckTimeout?.cancel();
        emit(const Unauthenticated());
        return;
      }

      // Récupérer l'utilisateur
      final result = await _getCurrentUserUseCase();

      result.fold(
        (failure) {
          _authCheckTimeout?.cancel();
          emit(const Unauthenticated());
        },
        (user) {
          _authCheckTimeout?.cancel();
          // On n'a pas le token ici, mais ce n'est pas grave
          // Il est déjà stocké localement
          emit(Authenticated(user: user, token: ''));
        },
      );
    } catch (e) {
      _authCheckTimeout?.cancel();
      emit(const Unauthenticated());
    }
  }

  // ==========================================================================
  // AUTO LOGOUT (session expirée)
  // ==========================================================================

  Future<void> _onAutoLogoutTriggered(
    AutoLogoutTriggered event,
    Emitter<AuthState> emit,
  ) async {
    // Pas de loading ici, déconnexion immédiate
    await _logoutUseCase();
    emit(const Unauthenticated());
  }
}