import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';

import 'app/core/di/service_locator.dart';
import 'app/core/routing/app_router.dart';
import 'app/core/themes/app_theme.dart';
import 'app/core/themes/theme_cubit.dart';
import 'app/features/auth/presentation/bloc/auth_bloc.dart';
import 'app/features/auth/presentation/bloc/auth_state.dart';

void main() async {
  WidgetsBinding widgetsBinding = WidgetsFlutterBinding.ensureInitialized();
  FlutterNativeSplash.preserve(widgetsBinding: widgetsBinding);

  await initializeDependencies();
  await initializeDateFormatting('fr_FR', null);

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider<AuthBloc>(create: (_) => sl<AuthBloc>()),
        BlocProvider<ThemeCubit>(create: (_) => sl<ThemeCubit>()),
      ],
      child: const _AppView(),
    );
  }
}

class _AppView extends StatefulWidget {
  const _AppView();

  @override
  State<_AppView> createState() => _AppViewState();
}

class _AppViewState extends State<_AppView> {
  late final GlobalKey<NavigatorState> _navigatorKey;
  late final AuthNotifier _authNotifier;
  late final GoRouter _router;

  @override
  void initState() {
    super.initState();
    _navigatorKey = sl<GlobalKey<NavigatorState>>();
    // AuthNotifier écoute le AuthBloc et notifie GoRouter à chaque changement
    _authNotifier = AuthNotifier(context.read<AuthBloc>());
    // Le router est créé UNE SEULE FOIS — pas de rebuild intempestif
    _router = AppRouter.createRouter(
      authNotifier: _authNotifier,
      navigatorKey: _navigatorKey,
    );
  }

  @override
  void dispose() {
    _authNotifier.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Seul le changement de thème provoque un rebuild ici
    return BlocBuilder<ThemeCubit, ThemeMode>(
      builder: (context, themeMode) {
        return MaterialApp.router(
          title: 'Code Ascend',
          debugShowCheckedModeBanner: false,
          theme: AppTheme.lightTheme,
          darkTheme: AppTheme.darkTheme,
          themeMode: themeMode,
          routerConfig: _router,
        );
      },
    );
  }
}

/// Pont entre AuthBloc et GoRouter.
///
/// Chaque changement d'état du AuthBloc appelle notifyListeners(),
/// ce qui déclenche la réévaluation du redirect dans GoRouter.
/// C'est ce mécanisme qui déblocait la splash screen.
class AuthNotifier extends ChangeNotifier {
  final AuthBloc _bloc;
  late final StreamSubscription<AuthState> _sub;
  AuthState _state;

  AuthNotifier(this._bloc) : _state = _bloc.state {
    _sub = _bloc.stream.listen((newState) {
      _state = newState;
      notifyListeners(); // GoRouter réévalue redirect()
    });
  }

  AuthState get state => _state;
  bool get isAuthenticated => _state is Authenticated;

  @override
  void dispose() {
    _sub.cancel();
    super.dispose();
  }
}