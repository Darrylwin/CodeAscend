import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';
import 'app/core/di/service_locator.dart';
import 'app/core/routing/app_router.dart';
import 'app/core/themes/app_theme.dart';
import 'app/core/themes/theme_cubit.dart';
import 'app/features/auth/presentation/bloc/auth_bloc.dart';
import 'app/features/auth/presentation/bloc/auth_state.dart';

void main() async {
  //  Garder le splash natif visible
  WidgetsBinding widgetsBinding = WidgetsFlutterBinding.ensureInitialized();
  FlutterNativeSplash.preserve(widgetsBinding: widgetsBinding);

  // Initialiser les dépendances (GetIt)
  await initializeDependencies();

  // Initialiser les locales pour le formatage des dates
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

/// Widget séparé pour gérer le router et le thème
class _AppView extends StatefulWidget {
  const _AppView();

  @override
  State<_AppView> createState() => _AppViewState();
}

class _AppViewState extends State<_AppView> {
  late final GlobalKey<NavigatorState> _navigatorKey;

  @override
  void initState() {
    super.initState();
    _navigatorKey = sl<GlobalKey<NavigatorState>>();
  }

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<ThemeCubit, ThemeMode>(
      builder: (context, themeMode) {
        return BlocBuilder<AuthBloc, AuthState>(
          buildWhen: (previous, current) {
            // Reconstruire uniquement si l'état d'authentification change
            final wasAuthenticated = previous is Authenticated;
            final isAuthenticated = current is Authenticated;
            return wasAuthenticated != isAuthenticated;
          },
          builder: (context, authState) {
            final isAuthenticated = authState is Authenticated;

            final router = AppRouter.router(
              isAuthenticated: isAuthenticated,
              authState: authState,
              navigatorKey: _navigatorKey,
            );

            return MaterialApp.router(
              title: 'Code Ascend',
              debugShowCheckedModeBanner: false,
              theme: AppTheme.lightTheme,
              darkTheme: AppTheme.darkTheme,
              themeMode: themeMode,
              routerConfig: router,
            );
          },
        );
      },
    );
  }
}
